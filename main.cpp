#include <iostream>

#include "GLWrap.h"

#include "testSim.h"

int main()	{
	unsigned int particleCount=1200;
	unsigned int dimensionCount=2;

	GLWrap test(particleCount,dimensionCount);
	testSim testSimObj(particleCount);	
	//testSimObj.timeStep();
	while(!test.getExitAnimation())	{
	    testSimObj.timeStep();
	    //std::cout << testSimObj.getPosBuffer()<<std::endl;	    
	    test.updateScreen(testSimObj.getPosBuffer());
	    //std::cin.get();	
	}
	test.exitWindow();

	
	return 0 ;
}







