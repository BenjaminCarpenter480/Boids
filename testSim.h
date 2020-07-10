/*
 *
 * TODO: RENAME position struct to vector
 *
 */


#include <cmath>
class testSim   {
    private:
        struct position {
            double x;
            double y;
        };
        position * posL;
        float dt = 0.5;
       /*
        void normalisePos() {
            double maxDist = sqrt(pow(posL[0].x,2)+pow(posL[0].y,2)); 
            for (int i = 1; i < sizeof(posL)/sizeof(position) ; i++) {
                 //TODO
            }
        }
        */
    public:
        unsigned int numOfParticles;
        const unsigned int dimensionality = 2;
        double * getPosBuffer() {
            //Returns a buffer from posL list
            double * retBuffer = new double[numOfParticles*dimensionality];
            unsigned int c = 0;
            for (int i = 1; i < sizeof(posL)/sizeof(position) ; i++) {
                retBuffer[c] = posL[i].x;
                c++;
                retBuffer[c] = posL[i].y;
                c++;
        }
        return retBuffer;
        }

        unsigned int findNearestNeighbour(unsigned int index)    {
            double maxDist = sqrt(pow(posL[0].x,2)+pow(posL[0].y,2)); 
            unsigned int nnIndex = 0;
            for (int i = 1; i < sizeof(posL)/sizeof(position) ; i++) {
                double currentDist = sqrt(pow(posL[0].x,2)+pow(posL[0].y,2))  ; 
                if (maxDist< currentDist)  {
                    maxDist = currentDist;
                    nnIndex = i;
                }
            }
            return nnIndex;
        }

        position moveAwayDir(unsigned int x, unsigned int y)    {
        //MOVE PERPENDICULAR TO Nearest neighbour
            position retPos;
            retPos.y = -1*x/y;
            retPos.x = 1/sqrt(1+pow(retPos.y,2));
            return retPos;
        }


        position moveAwayDir(position posAwayFrom)  {
            return moveAwayDir(posAwayFrom.x,posAwayFrom.y);
        }

        
        void timeStep() {//Position updater function
            for (int i= 0; i< sizeof(posL)/sizeof(position);i++)    {
                unsigned int nnIndex = findNearestNeighbour(i);
                position dir = moveAwayDir(posL[nnIndex].x,posL[nnIndex].y);
                posL[i].x = posL[i].x+dir.x;
                posL[i].y = posL[i].y+dir.y;

            }
         
        }


        double * updatePositions()  {
            timeStep();
            return getPosBuffer();
        }



        testSim(unsigned int particleCount) {
            
            posL = new position[particleCount];
            for (int i= 0; i< sizeof(posL)/sizeof(position);i++)    {
                posL[i].x = rand()%100;
                posL[i].y = rand()%100;
            }
        }
        



};
