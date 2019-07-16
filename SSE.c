#include "stdio.h"
#include "stdlib.h"
#include "nmmintrin.h"

//useful don't change
float *meargeFuncFloat(float pic1[4], float pic2[4]){
	
	__attribute__((aligned(16))) float fpix1[4];
	__attribute__((aligned(16))) float fpix2[4];
	
	for(int i=0; i<4; i++){
		fpix1[i] = pic1[i];
		fpix2[i] = pic2[i];
		//printf("fpix1[%d]=%lf,fpix2[%d]=%lf\n",i,fpix1[i],i,fpix2[i]);
	}
	/*
	*/
		
	__m128 pix1;
	__m128 pix2;
	__m128 pixMearge;

	float ret[4];

	pix1 = _mm_load_ps(fpix1);
	pix2 = _mm_load_ps(fpix2);
	
	pixMearge = _mm_add_ps(pix1, pix2);
	//printf("pixMearge:%f",pixMearge);
	_mm_store_ps(ret, pixMearge);

	
	
	float *p = ret;
	/*
	for(int i=0; i<4; i++){
		printf("*(p+%d)=%lf\n",i, *(p+i));
	}
	*/
	return p;
}

//retType = int
int *meargeFunc(int pic1[4], int pic2[4], float fadeRate){
	
	//__attribute__((aligned(16))) float _fpix1[4];
	//__attribute__((aligned(16))) float _fpix2[4];
	__attribute__((aligned(16))) float _fadeRate[4] = {fadeRate,fadeRate,fadeRate,fadeRate};
	__attribute__((aligned(16))) float _fpix1[4] = {(float)pic1[0],(float)pic1[1],(float)pic1[2],(float)pic1[3]};
	__attribute__((aligned(16))) float _fpix2[4] = {(float)pic2[0],(float)pic2[1],(float)pic2[2],(float)pic2[3]};
	
	//_fpix1 = _mm_cvtepi16_ps(pic1)
	//_fpix2 = _mm_cvtepi16_ps(pic2)

	/*
	for(int i=0; i<4; i++){
		//_fpix1[i] = (float)pic1[i];
		//_fpix2[i] = (float)pic2[i];
		_fadeRate[i] = fadeRate;
		//printf("fpix1[%d]=%lf,fpix2[%d]=%lf\n",i,fpix1[i],i,fpix2[i]);
	}
	
	
	*/
		
	__m128 _pix1;
	__m128 _pix2;
	__m128 _fade;
	__m128 _pixSub;
	__m128 _pixMul;
	__m128 _pixRet;

	__attribute__((aligned(16))) int _ret[4];
	/*
	_pix1 = _mm_load_ps(_fpix1);
	_pix2 = _mm_load_ps(_fpix2);
	_fade = _mm_load_ps(_fadeRate);
	
	_pixSub = _mm_sub_ps(_pix1, _pix2);  //pixa - pixb
	_pixMul = _mm_mul_ps(_pixSub, _fade);//ans * fade
	_pixRet = _mm_add_ps(_pixMul, _pix2);//ans + pixb = resultPixel
	*/
	//printf("pixMearge:%f",pixMearge);

	_pix1 = _mm_loadu_ps(_fpix1);
	_pix2 = _mm_loadu_ps(_fpix2);
	_fade = _mm_load_ps(_fadeRate);
	
	_pixSub = _mm_sub_ps(_pix1, _pix2);  //pixa - pixb
	_pixMul = _mm_mul_ps(_pixSub, _fade);//ans * fade
	_pixRet = _mm_add_ps(_pixMul, _pix2);//ans + pixb = resultPixel

	__m128i _intRet;
	
	_intRet = _mm_cvttps_epi32(_pixRet);//convert float to int

	_mm_store_si128(_ret, _intRet);//store int type result

	
	int *p = _ret;
	/*	
	for(int i=0; i<4; i++){
		printf("*(p+%d)=%d\n",i, *(p+i));
	}
	
	*/
	return p;
}



int *meargeFun(int pic1[4], int pic2[4]){
	for(int i=0; i<4; i++){
		printf("pic1[%d]=%d\n",i, pic1[i]);	
	}
	for(int i=0; i<4; i++){
		printf("pic2[%d]=%d\n",i, pic2[i]);	
	}
	int mearge[4];
	for(int i=0; i<4; i++){
		mearge[i] = pic1[i] + pic2[i];
		printf("mearge[%d]=%d\n",i,mearge[i]);	
	}
	int *p = mearge;
	/*for(int i=0;i<4;i++){
		printf("%d",*(p+i));
	}*/
	return p;
	
}

int *meargeFun2(int *pic1, int *pic2){
	for(int i=0; i<4; i++){
		printf("pic1[%d]=%d\n",i, *(pic1+i));	
	}
	for(int i=0; i<4; i++){
		printf("pic2[%d]=%d\n",i, *(pic2+i));	
	}
	int *mearge;
	for(int i=0; i<4; i++){
		*(mearge+i) = *(pic1+i) + *(pic2+i);
	}
	return  mearge;	
}

