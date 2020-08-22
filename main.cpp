#include <iostream>

#include "GLWrap.h"

#include "Boids.h"

#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif



int main()	{
	const unsigned int particleCount= 200; //IS actually a few less than this
	
	const unsigned int dimensionCount=2;
	
	const double dt_speed = 100;//REUNDANT, CONSIDER REMOVAL, Constant on the stepsize as movement is done on unit method
	const int k=10;//Density effectively (higher k lower density)
	 
	GLWrap test(particleCount,dimensionCount);

	Boids testSimObj(particleCount,dt_speed,k);	

	while(!test.getExitAnimation())	{
	    testSimObj.timeStep();
	   
	    //std::cout << testSimObj.getPosBuffer()<<std::endl;	    
		
		//Clear, send and draw GPU operations
		test.screenClear();
		test.draw(testSimObj.getBuffer());
		test.updateScreen();
        usleep(40000); //Adds 25 fps limit
	
	

	}
	test.exitWindow();

	
	return 0 ;
}







