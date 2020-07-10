#include <iostream>

#include "GLWrap.h"

#include "testSim.h"

int main()	{
	unsigned int particleCount=3;
	unsigned int dimensionCount=2;

	GLWrap test(particleCount,dimensionCount);
	testSim testSimObj(particleCount);	
	test.setPositionUpdateFunction(testSimObj.updatePositions);	
	test.simLoop();
	return 0 ;
}







