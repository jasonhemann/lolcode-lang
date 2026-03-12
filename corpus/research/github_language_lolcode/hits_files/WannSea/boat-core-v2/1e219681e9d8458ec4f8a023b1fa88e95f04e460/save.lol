use std::sync::{Arc, RwLock};
use std::time::{UNIX_EPOCH, SystemTime};

use log::{debug, trace, warn};
use tokio::sync::broadcast::error::RecvError;
use tokio::sync::broadcast::Sender;
use tokio::sync::{broadcast, Mutex};
use wannsea_types::MessageId;
use wannsea_types::boat_core_message::Value;

use crate::helper::{MetricSender, MetricSenderExt};

#[derive(Clone)]
pub struct MetricStats {
    pub len: usize,
    pub last_ts: u128,
    pub metrics_in_per_sec: f32,
    pub metrics_out_per_sec: f32,
    pub metrics_in: usize,
    pub metrics_out: usize
}

pub struct MetricQueue<T> {
    metric_sender: MetricSender,
    queue: Arc<RwLock<Vec<T>>>,
    stats: Arc<RwLock<MetricStats>>
}

impl<T> MetricQueue<T> where T: Clone + std::fmt::Debug + Sized {
    pub fn new(metric_sender: MetricSender) -> Self {
        Self {
            metric_sender,
            queue: Arc::new(RwLock::new(Vec::new())),
            stats: Arc::new(RwLock::new(MetricStats { len: 0, last_ts: 0, metrics_in_per_sec: 0.0, metrics_out_per_sec: 0.0, metrics_in: 0, metrics_out: 0 }))
        }
    }

    fn calc_stats(&self, mut stats: std::sync::RwLockWriteGuard<'_, MetricStats, >) {
        let ts = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_millis();
        if ts - stats.last_ts > 1000 {
            stats.metrics_in_per_sec = stats.metrics_in as f32;
            stats.metrics_out_per_sec = stats.metrics_out as f32;
            stats.metrics_in = 0;
            stats.metrics_out = 0;
            stats.last_ts = ts;
            self.metric_sender.send_now(MessageId::TxQueueCount, Value::Uint64(stats.len as u64)).unwrap();
            self.metric_sender.send_now(MessageId::TxInPerSec, Value::Float(stats.metrics_in_per_sec as f32)).unwrap();
            self.metric_sender.send_now(MessageId::TxOutPerSec, Value::Float(stats.metrics_out_per_sec as f32)).unwrap();
        }
    }

    pub fn push(&self, e: T) {
        self.queue.write().unwrap().push(e);
        let mut stats = self.stats.write().unwrap();
        stats.len += 1;
        stats.metrics_in += 1;
        self.calc_stats(stats);
    }

    pub async fn pop(&self) -> Vec<T> {
        let q_handle = self.queue.write().unwrap();

        let mut stats = self.stats.write().unwrap();
        stats.len = q_handle.len();
        stats.metrics_out += 1;
        self.calc_stats(stats);

        return q_handle.clone();
    }
}


============



use std::{sync::Arc, time::{SystemTime, UNIX_EPOCH}};

use futures::{StreamExt, SinkExt};
use log::{debug, info, warn};
use tokio::sync::RwLock;
use tokio_tungstenite::connect_async;
use wannsea_types::{boat_core_message::Value, BoatCoreMessage, MessageId};
use prost::Message;
use crate::{helper::{MetricSender, MetricSenderExt}, SETTINGS};

use super::metric_queue::MetricStats;

pub struct WebSocketClient {
    metric_sender: MetricSender,
    cached_messages: Arc<RwLock<Vec<BoatCoreMessage>>>,
    stats: Arc<RwLock<MetricStats>>,
} 


impl WebSocketClient {
    pub fn new(metric_sender: MetricSender) -> Self {
        WebSocketClient { metric_sender: metric_sender.clone(), cached_messages: Arc::new(RwLock::new(Vec::new())), stats: Arc::new(RwLock::new(MetricStats { len: 0, last_ts: 0, metrics_in_per_sec: 0.0, metrics_out_per_sec: 0.0, metrics_in: 0, metrics_out: 0 })) }
    }

    async fn start_thread(stats_l: Arc<RwLock<MetricStats>>, metric_queue: Arc<RwLock<Vec<BoatCoreMessage>>>) {
        loop {        
            debug!("Trying to connect to ws...");
            let addr = SETTINGS.get::<String>("ws-client.address").unwrap().to_string();
            let retry_timeout = SETTINGS.get::<u64>("ws-client.retry_timeout").unwrap();
            let timeout_dur = tokio::time::Duration::from_millis(retry_timeout);
            let timeout_res = tokio::time::timeout(timeout_dur, connect_async(&addr)).await;
            if timeout_res.is_err() {
                debug!("Could not reach the WebSocket server at {}. Retrying in {} ms...", &addr, retry_timeout);
                tokio::time::sleep(timeout_dur).await;
                continue;
            }
            
            let websocket_res = timeout_res.unwrap();
            if let Err(websocket_err) = websocket_res {
                debug!("Error opening WebSocket {:?}",websocket_err);
                tokio::time::sleep(timeout_dur).await;
                continue;
            }

            info!("WebSocket handshake has been successfully completed");

            let (mut write, _read) = websocket_res.unwrap().0.split();
            
            'connection_loop: loop {
                tokio::time::sleep(tokio::time::Duration::from_millis(SETTINGS.get::<u64>("ws-client.poll_interval").unwrap())).await;
                let mut q_handle = metric_queue.write().await;
                let send_batch = q_handle.clone();
                q_handle.clear();

                let mut stats = stats_l.write().await;
                let q_size: usize = send_batch.len();
                for msg in send_batch {
                    let mut buf = Vec::new();
                    buf.reserve(msg.encoded_len());
                    msg.encode(&mut buf).unwrap();
                    let send_result = write.send(tokio_tungstenite::tungstenite::Message::Binary(buf)).await;
                    match send_result {
                        Ok(_res) => {
                            stats.metrics_out += 1;
                        },
                        Err(err) => {
                            warn!("Couldnt send metric: {:?}", err);
                            q_handle.push(msg);
                            break 'connection_loop;
                        }
    
                    }
                }
                debug!("Sent {} messages", q_size);     
            }
        }
    }

    pub async fn report_thread(metric_sender: MetricSender, stats_l: Arc<RwLock<MetricStats>>) {
        loop {
            tokio::time::sleep(tokio::time::Duration::from_millis(1000)).await;
            let mut stats = stats_l.write().await;
            let ts = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_millis();
            if ts - stats.last_ts > 1000 {
                stats.metrics_in_per_sec = stats.metrics_in as f32;
                stats.metrics_out_per_sec = stats.metrics_out as f32;
                stats.metrics_in = 0;
                stats.metrics_out = 0;
                stats.last_ts = ts;
                metric_sender.send_now(MessageId::TxQueueCount, Value::Uint64(stats.len as u64)).unwrap();
                metric_sender.send_now(MessageId::TxInPerSec, Value::Float(stats.metrics_in_per_sec as f32)).unwrap();
                metric_sender.send_now(MessageId::TxOutPerSec, Value::Float(stats.metrics_out_per_sec as f32)).unwrap();
            }
        }   

    }

    pub async fn fill_queue_thread(metric_sender: MetricSender, stats_l: Arc<RwLock<MetricStats>>, metric_queue: Arc<RwLock<Vec<BoatCoreMessage>>> ) {
        let mut receiver = metric_sender.subscribe();
        loop {
            match receiver.recv().await {
                Ok(msg) => {
                    let mut q_handle = metric_queue.write().await;
                    q_handle.push(msg);
                    stats_l.write().await.metrics_in = q_handle.len();
                },
                Err(err) => warn!("Error while receiving from Metric Bus: {:?}", err),
            }
        }
    }

    pub fn start(&self) {
        if SETTINGS.get::<bool>("ws-client.enabled").unwrap() {
            info!("WebSocket Client enabled!");

            tokio::spawn(Self::start_thread( self.stats.clone(), self.cached_messages.clone()));
            tokio::spawn(Self::report_thread(self.metric_sender.clone(), self.stats.clone()));
            tokio::spawn(Self::fill_queue_thread(self.metric_sender.clone(), self.stats.clone(), self.cached_messages.clone()));
            
        }


    }
}