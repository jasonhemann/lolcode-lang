\babel@toc {english}{}\relax 
\addvspace {10\p@ }
\addvspace {10\p@ }
\addvspace {10\p@ }
\addvspace {10\p@ }
\addvspace {10\p@ }
\addvspace {10\p@ }
\addvspace {10\p@ }
\addvspace {10\p@ }
\addvspace {10\p@ }
\addvspace {10\p@ }
\addvspace {10\p@ }
\addvspace {10\p@ }
\contentsline {listing}{\numberline {5.1}{\ignorespaces The \texttt {AppState} struct that holds all relevant shared states}}{48}{listing.5.1}%
\contentsline {listing}{\numberline {5.2}{\ignorespaces The substates \texttt {SharedDBState} and the \texttt {SharedGraphState} that make up the \texttt {AppState}}}{49}{listing.5.2}%
\contentsline {listing}{\numberline {5.3}{\ignorespaces The implementation of \texttt {FromRef<AppState>} for the two substates}}{50}{listing.5.3}%
\contentsline {listing}{\numberline {5.4}{\ignorespaces A collection of API routes for this project with their respective URLs and their functions}}{50}{listing.5.4}%
\contentsline {listing}{\numberline {5.5}{\ignorespaces One of the wrapper functions that manage a call to an \acrshort {code:api} route (in this case \texttt {http://127.0.0.1:8881/api/update\_project\_id})}}{51}{listing.5.5}%
\contentsline {listing}{\numberline {5.6}{\ignorespaces The request body of a request going to \texttt {http://127.0.0.1:8881/api/update\_project\_id} using the \texttt {REST POST} method}}{52}{listing.5.6}%
\contentsline {listing}{\numberline {5.7}{\ignorespaces The instantiation of the connection pool to the database using \textit {sqlx}'s built-in functions \texttt {PgPoolOptions::new()} and \texttt {PgPoolOptions::connect(url: \&str)}}}{54}{listing.5.7}%
\contentsline {listing}{\numberline {5.8}{\ignorespaces The structs \texttt {Graph}, \texttt {Vertex} and \texttt {Tray}}}{58}{listing.5.8}%
\contentsline {listing}{\numberline {5.9}{\ignorespaces The declaration of the min-priority queue \texttt {heap} and the hashmap \texttt {distance}}}{59}{listing.5.9}%
\contentsline {listing}{\numberline {5.10}{\ignorespaces The traits \texttt {PartialOrd} and \texttt {Ord} implemented for the struct \texttt {State}}}{59}{listing.5.10}%
\contentsline {listing}{\numberline {5.11}{\ignorespaces The initialization of the \texttt {HashMap} and the \texttt {Queue} with the start vertex}}{60}{listing.5.11}%
\contentsline {listing}{\numberline {5.12}{\ignorespaces The loop that moves the currently visited vertex using the min-priority queue}}{60}{listing.5.12}%
\contentsline {listing}{\numberline {5.13}{\ignorespaces The final loop collecting all edges from the currently visited vertex and parsing them into \textit {Dijkstra}}}{61}{listing.5.13}%
\contentsline {listing}{\numberline {5.14}{\ignorespaces The loop relaxing each edge $|V|-1$ times, and collecting the resulting path into a length and \texttt {Vector} of \texttt {Trays}}}{63}{listing.5.14}%
\contentsline {listing}{\numberline {5.15}{\ignorespaces The impact of the heuristic on the implementation of the \textit {A*} algorithm}}{64}{listing.5.15}%
\contentsline {listing}{\numberline {5.16}{\ignorespaces The stopping condition of bidirectional \textit {Dijkstra}/\textit {A*}}}{66}{listing.5.16}%
\contentsline {listing}{\numberline {5.17}{\ignorespaces The trigger function of the database to check if the two vertices of a tray are different (function \texttt {check\_if\_same\_vertex()}}}{71}{listing.5.17}%
\contentsline {listing}{\numberline {5.18}{\ignorespaces The creation of the trigger with the underlying function}}{71}{listing.5.18}%
\addvspace {10\p@ }
\addvspace {10\p@ }
\addvspace {10\p@ }
\addvspace {10\p@ }
\addvspace {10\p@ }
\addvspace {10\p@ }
\addvspace {10\p@ }
\addvspace {10\p@ }
\contentsline {listing}{\numberline {A.1}{\ignorespaces One the functions that handle an API call to \texttt {http://127.0.0.1:8881/api/generate\_project} directly called by the router}}{96}{listing.A.1}%
\contentsline {listing}{\numberline {A.2}{\ignorespaces One of the functions that handle an API call to \texttt {http://127.0.0.1:8881/api/generate\_project} directly generating the project}}{97}{listing.A.2}%
\contentsline {listing}{\numberline {A.3}{\ignorespaces The function reconstructing the path for each algorithm}}{98}{listing.A.3}%
\contentsline {listing}{\numberline {A.4}{\ignorespaces The function that finds any edge going to or from an edge}}{99}{listing.A.4}%
\contentsline {listing}{\numberline {A.5}{\ignorespaces The function that updates the occupancy of a given tray path for a cable with given diameter}}{99}{listing.A.5}%
