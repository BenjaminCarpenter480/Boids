#include <iostream>

#include "GLWrap.h"

#include "testSim.h"

#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif



int main()	{
	const unsigned int particleCount= 200; //IS actually a few less than this
	const unsigned int dimensionCount=2;
	const double dt_speed = 100;//Constant on the stepsize as movement is done on unit method
	const int k=100;//Density effectively (higher k lower density)
	const float SLEEP_C= 0.95;//COnst on time to sleep to improve visibility
	GLWrap test(particleCount,dimensionCount);

	testSim testSimObj(particleCount,dt_speed,k);	

	while(!test.getExitAnimation())	{
	    testSimObj.timeStep();
	   
	    //std::cout << testSimObj.getPosBuffer()<<std::endl;	    
		test.screenClear();
		test.draw(testSimObj.getBuffer());
		test.updateScreen();
	    usleep(40000); //Adds 25 fps calc
	
	

	}
	test.exitWindow();

	
	return 0 ;
}







