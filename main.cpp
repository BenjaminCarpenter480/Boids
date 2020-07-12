#include <iostream>

#include "GLWrap.h"

#include "testSim.h"

#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif



int main()	{
	const unsigned int particleCount=4; //IS actually a few less than this
	const unsigned int dimensionCount=2;
	const double dt_speed = 1;//Constant on the stepsize as movement is done on unit method
	const int k=100;//Density effectively (higher k lower density)
	const float SLEEP_C= 0.95;//COnst on time to sleep to improve visibility
	GLWrap test(particleCount,dimensionCount);
	
			//             SPEDD,Konst
	testSim testSimObj(particleCount,dt_speed,k);	
	//testSimObj.timeStep();
	while(!test.getExitAnimation())	{
	    testSimObj.timeStep();
	    //std::cout << testSimObj.getPosBuffer()<<std::endl;	    
	    test.updateScreen(testSimObj.getPosBuffer());
	    sleep(0.95);
	    //std::cin.get();
	}
	test.exitWindow();

	
	return 0 ;
}







