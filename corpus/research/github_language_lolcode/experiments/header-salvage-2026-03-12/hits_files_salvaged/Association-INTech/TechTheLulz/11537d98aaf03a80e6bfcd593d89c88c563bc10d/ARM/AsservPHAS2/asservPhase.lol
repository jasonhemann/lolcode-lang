//#include "my_io.c"
#include <math.h>

int __errno;//CECI EST UN GROS HACK TOUT MOCHE, MAIS SINON CA COMPILE PAS.

#define CONST_LOLG 1.0/12000.0
#define CONST_LOLD 1.0/12000.0

//#define INV_MOT_G
#define INV_MOT_D


//C'est un asserv en trois phases (tourner-avancer-tourner), plus conventionnel, moins lol
char phase=1;

#define PI 3.14159265359

#define ABS(x) (x<0?-x:x)

#define SEUIL_UTILITE_PWM 700.0
#define SEUIL_MAX_PWM 1500.0
#define PREC_ANGLE1 0.3
#define PREC_ANGLE2 0.01
#define PREC_POS 0.10


	 int couper_moteurs=1;

	 double dist_seuil_autorisation_marche_arriere=0.05;
	 double pas_accel=0.2;
	 double coefftrans1=-2000.0;
	 double coefftrans2=10;
	 double coeffrot=3000.0;
	 double maxtrans=255;
	 double dist_seuil_avant_tourner=0.15;
	 double coeff_courbure_but=0.35;
	 
	 long pas_accel2=5;
	 long pas_accel2P3=50;
	 

//grandeurs en metres

	 double circon_G = 0.06;              //circonference roue gauche
	 double circon_D = 0.06;
	 double tics_t_G = 360;            //tics/tour codeur gauche
	 double tics_t_D = 360;
	 double diam_robot = 0.30;         //largeur du robot (ecart entre les deux roues)

//protection anti-delire pour l'arduino : seuil a ne pas depasser en tics par microseconde
#define LOLMAX 5

#define MASQUE B0111100

//coordonnees du robot
	 double angle=0;
	 double x = 0;
	 double y = 0;

//consignes
	 double c_angle=0;
	 double c_x = 0;
	 double c_y = 0;

	 double c_trans=0;
	 double c_rot=0;

	 int p_g=0;
	 int p_d=0;


// // 	 volatile long int tics_G=0;
// // 	 volatile long int tics_D=0;

// // 	 unsigned long int prec_correct_interval=0;
// // 	 unsigned long int prec_correct=0;
// // 	 unsigned long int prec_mauvais=0;
// // 	 int prec_tics_G=0;
// // 	 int prec_tics_D=0;

	 double dist(double x1,double y1,double x2,double y2);
	 double angl(double x1,double y1,double x2,double y2);
	 void calc_consignes();
	 void app_consignes();


	 double posGprev=0,posDprev=0;
	 void actualiser_coords()
	 {
	 	filtres_codeurs();
//	 	my_printf("lol%f %f %f %f \n",codeur_filtred1,posGprev,codeur_filtred2,posDprev);
		 double prevangle=angle; //angle utilise pour la moyenne dans le calcul d'odometrie
		 double tG=-codeur_filtred1-posGprev;//=codeur[0].tics;
		 double tD=codeur_filtred2-posDprev;//=codeur[1].tics;
		 double delta_T_G = tG*CONST_LOLG;
		 double delta_T_D = tD*CONST_LOLD;
  		 
  		 posGprev=-codeur_filtred1;
  		 posDprev=codeur_filtred2;
  		 
		 //codeur[0].tics=0;
		 //codeur[1].tics=0;

		 angle += (delta_T_G - delta_T_D)/diam_robot;

		 double delta_t= (delta_T_G + delta_T_D)/2.0;
  
		 double angle_m=(prevangle+angle)/2; //moyenne du nouvel angle et du precedent
  
		 double am=angle_m;
		 double sin_angle_m = sin(am);
		 double cos_angle_m = cos(am);
		 
		 x += delta_t*cos_angle_m;
		 y += delta_t*sin_angle_m; 
	 }

	 char i;

	 void loop()
	 {
		 actualiser_coords();
  //delay(1000);
		 calc_consignes();
		 app_consignes();
  
		 if(!(i++))
		 {
/*  
			 Serial.print("tics_G ");
			 Serial.print(tics_G);
			 Serial.print(" tics_D ");
			 Serial.print(tics_D);
  
			 Serial.print(" X = ");
			 Serial.print((x)*100.0);
			 Serial.print(" Y = ");
			 Serial.print((y)*100.0);
			 Serial.print(" angle = ");
			 Serial.print(angle*180.0/3.14159265359);
  
			 Serial.print(" c_rot=");
			 Serial.print(c_rot);
			 Serial.print(" c_trans=");
			 Serial.print(c_trans);
  
			 Serial.print(" p_g=");
			 Serial.print(p_g);
			 Serial.print(" p_d=");
			 Serial.println(p_d);
  
 */ 
 
  //Serial.print("phase ");
//  Serial.println((int)phase);
  
			}
	 }

int fiter=0;

	 void calc_consignes()
	 { 
	 	 fiter++;
 		 couper_moteurs=0;
		 int sens=1;
        //translation
		 double temptrans = dist(x,y,c_x,c_y);
//		 my_printf("D%f\n",temptrans);
		 double tempangle;
		 double diff;
		 double angle_vers_cible= angl(x,y,c_x,c_y);
        //my_printf("a:%f ca:%f avc:%f p:%d\n",angle,c_angle,angle_vers_cible,phase);
        //Serial.println(angle);
		 double val_comp=phase==3?PREC_POS:PREC_POS/4.0;//evite d'etre coince entre phase 2 et 3
//		 my_printf("VC%f\n",val_comp);
		 
		 if(temptrans<val_comp)
		 {
			 phase=3;
			 if(ABS(angle_modulo(c_angle-angle))<PREC_ANGLE1)
			 {
				 couper_moteurs=1;
				 //my_printf("lol\n");
				 phase=4;
			 }
			 tempangle=c_angle;
			 temptrans=0;
		 }
		 else 
		 {
		 	 //my_printf("else couper_moteurs=%d\n",couper_moteurs);
			 diff=ABS(angle_modulo(angle_vers_cible-angle));
			 if(diff>1.57079633)
			 {
				 angle_vers_cible+=PI;
				 sens=-1;
				 diff=PI-diff;
			 }
			 tempangle=angle_vers_cible;
	
			 if(diff>PREC_ANGLE2)
			 {          
				 phase=1;
				 temptrans=0;
			 }
			 else
			 {
				 phase=2;
			 }
		 }
		 c_rot=angle_modulo(tempangle-angle);
		 temptrans*=coefftrans1;
		 temptrans*=sens;
	//c_trans=temptrans;
		 int s1=signe(c_trans);
		 int s2=signe(temptrans);
	
		 if((s1*s2)<0)
		 {
			 if(s2==-1)
				 c_trans=-0.000001;
			 else
				 c_trans=0.000001;
		 }
		 if(c_trans>=0.0)
		 {
			 if(c_trans>temptrans)
				 c_trans=temptrans;
			 else if (c_trans<temptrans)
				 c_trans+=pas_accel;
		 }
		 else
		 {
			 if(c_trans<temptrans)
				 c_trans=temptrans;
			 else if(c_trans>temptrans)
				 c_trans-=pas_accel;
		 }
	
	//printf("temptrans=%f, trans=%f , cas=%d\n", temptrans, c_trans, cas);
	
		 if(c_trans>maxtrans)
			 c_trans=maxtrans;
		 if(c_trans<-maxtrans)
			 c_trans=-maxtrans;
	 }

int sens_g;
int sens_d;
double c_g;
double c_d;

		 
	 void app_consignes()
	 {
	 	int exg=(signe(c_g)*p_g);
		int exd=(signe(c_d)*p_d);
		
		 if(couper_moteurs)
		 {
		 	 //my_printf("moteurs eteints\n");
			 TIM_SetCompare1(TIM3, 0);
			 TIM_SetCompare2(TIM3, 0);
			 return;
		 }
		 c_g=(c_trans*coefftrans2 - c_rot*coeffrot);
		 c_d=(c_trans*coefftrans2 + c_rot*coeffrot);
		 p_g=satur(ABS(c_g)+SEUIL_UTILITE_PWM,SEUIL_MAX_PWM);
		 p_d=satur(ABS(c_d)+SEUIL_UTILITE_PWM,SEUIL_MAX_PWM);
		
		 int ng=(signe(c_g)*p_g);
		 int nd=(signe(c_d)*p_d);
		 //my_printf("c_g=%f p_g=%d exg=%d ng=%d ",c_g,p_g,exg,ng);
		 //my_printf("c_d=%f p_d=%d exd=%d nd=%d ",c_d,p_d,exd,nd);
		 if(phase!=3)
		 {
			 if(ng > exg+pas_accel2)
				 ng=exg+pas_accel2;
			 else if(ng < exg-pas_accel2)
				 ng=exg-pas_accel2;
			 if(nd > exd+pas_accel2)
				 nd=exd+pas_accel2;
			 else if(nd < exd-pas_accel2)
				 nd=exd-pas_accel2;
		 }
		 else
		 {
			 if(ng > exg+pas_accel2P3)
				 ng=exg+pas_accel2P3;
			 else if(ng < exg-pas_accel2P3)
				 ng=exg-pas_accel2P3;
			 if(nd > exd+pas_accel2P3)
				 nd=exd+pas_accel2P3;
			 else if(nd < exd-pas_accel2P3)
				 nd=exd-pas_accel2P3;
		 }
		 //my_printf("nng=%d ",ng);
		 //my_printf("nnd=%d\n",nd);
		 
//		 c_g=ng;
//		 c_d=nd;
//		 p_g=ABS(ng);
//		 p_d=ABS(nd);
#ifdef INV_MOT_G
		 int sens_g=signe(c_g)==1?Bit_RESET:Bit_SET;
#else
		 int sens_g=signe(c_g)==1?Bit_SET:Bit_RESET;
#endif
#ifdef INV_MOT_D
		 int sens_d=signe(c_d)==1?Bit_SET:Bit_RESET;
#else
		 int sens_d=signe(c_d)==1?Bit_RESET:Bit_SET;
#endif
		 GPIO_WriteBit( GPIOA, GPIO_Pin_4, sens_g);
		 GPIO_WriteBit( GPIOA, GPIO_Pin_5, sens_d);
		 TIM_SetCompare1(TIM3, p_g);
		 TIM_SetCompare2(TIM3, p_d);
		// my_printf("c_t=%f c_r=%f\n",c_trans,c_rot,coefftrans2,coeffrot,c_g);
}

		   double dist(double x1,double y1,double x2,double y2)
		   {
			   double t1=x1-x2;
			   double t2=y1-y2;
			   return sqrt(t1*t1+t2*t2);
		   }

		   double angl(double x1,double y1,double x2,double y2)
		   {
			   return atan2(y2-y1,x2-x1);
		   }


		   volatile char etatPins = 0;



