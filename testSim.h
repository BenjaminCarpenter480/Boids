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
        float dt = 0.05;
    
        unsigned int particleCount;
        
        position* normalisePosArr() {
            double maxDistX = posL[0].x;
            double maxDistY = posL[0].y; 
            for (int i = 1; i < particleCount ; i++) {
                 if (maxDistX < posL[i].x)  {
                    maxDistX = posL[i].x;   
                 }
                 if (maxDistY <posL[i].y)   {
                     maxDistY = posL[i].y;
                }
            }
            position* posLRet = new position[particleCount];
            if(maxDistX>maxDistY)   {
                for (int i = 0; i < particleCount ; i++) {
                     posLRet[i].x = posL[i].x/maxDistX;
                     posLRet[i].y = posL[i].y/maxDistX;
                }
            }
            else    {
                for (int i = 0; i < particleCount ; i++) {
                    posLRet[i].x = posL[i].x/maxDistY;
                    posLRet[i].y = posL[i].y/maxDistY;
                }
            }
            return posLRet;
        }
    
    public:
        const unsigned int dimensionality = 2;
        double * getPosBuffer() {
            position * posLNorm = normalisePosArr();
            //Returns a buffer from posL list
            double * retBuffer = new double[particleCount*dimensionality];
            unsigned int c = 0;
            //std::cout<<"RETURN BUFFER"<<std::endl;
            for (int i = 0; i < particleCount ; i++) {
                retBuffer[c] = posLNorm[i].x;
                //std::cout<<retBuffer[c]<<",";
                c++;
                retBuffer[c] = posLNorm[i].y;
               // std::cout<<retBuffer[c]<<"\n";
                c++;
        }
        //std::cout<<"END RETURN BUFFER"<<std::endl;
        return retBuffer;
        }

        unsigned int findNearestNeighbour(unsigned int index)    {
            double maxDist = sqrt(pow(posL[0].x,2)+pow(posL[0].y,2)); 
            unsigned int nnIndex = 0;
            for (int i = 1; i < particleCount ; i++) {
                double currentDist = sqrt(pow(posL[i].x,2)+pow(posL[i].y,2))  ; 
                if (maxDist< currentDist)  {
                    maxDist = currentDist;
                    nnIndex = i;
                }
            }
            return nnIndex;
        }

        position moveAwayDir(unsigned int xS, unsigned int yS,unsigned int xT, unsigned int yT)    {
        //MOVE PERPENDICULAR TO Nearest neighbour
            position retPos;
            position diffs;
            diffs.x = xT-xS;
            diffs.y = yT-yS;
            retPos.y =  diffs.x; 
            retPos.x = -diffs.y;
            //retPos.x = retPos.x/sqrt(pow(diffs.x,2)   + pow(diffs.y,2));
            //retPos.y = retPos.y/sqrt(pow(diffs.x,2)   + pow(diffs.y,2));
             
            return retPos;
        }


        //position moveAwayDir(position posAwayFrom)  {
        //    return moveAwayDir(posAwayFrom.x,posAwayFrom.y);
        //}

        
        void timeStep() {//Position updater function
            std::cout<<"Timestep\n";
            for (int i= 0; i<particleCount/*sizeof(*posL)/sizeof(*position)*/;i++)    {
                unsigned int nnIndex = findNearestNeighbour(i);
                position dir = moveAwayDir(posL[i].x,posL[i].y,posL[nnIndex].x,posL[nnIndex].y);
                dir.x= ((rand()-RAND_MAX/2)%RAND_MAX/(double)RAND_MAX);
                 
                dir.y= ((rand()-RAND_MAX/2)%RAND_MAX/(double)RAND_MAX);

                //std::cout<<"diff" <<i<<std::endl;
                //std::cout<<"x"<<dir.x<<"\n"; 
                //std::cout<<"y"<<dir.y<<"\n";     
                //std::cout<<"-----------\n";
                
                //posL[i].x = posL[i].x+dir.x;
                //posL[i].y = posL[i].y+dir.y;
                

                posL[i].x = posL[i].x +dt*dir.x;
                posL[i].y = posL[i].y +dt*dir.y;
                //double mag = sqrt(pow(posL[i].x,2)+pow(posL[i].y,2));
                
                
                //posL[i].x = posL[i].x/mag;
                //posL[i].y = posL[i].y/mag;

                std::cout<<"P:"<<i<<std::endl;
                std::cout<<"dr:"<<dir.x<<","<<dir.y<<std::endl; 
                std::cout<<"Positions:"<<posL[i].x<<","<<posL[i].y<<std::endl;
                
            }
         
        }


        double * updatePositions()  {
            timeStep();
            return getPosBuffer();
        }



        testSim(unsigned int pparticleCount) {
            particleCount = pparticleCount;
            posL = new position[pparticleCount];
            for (int i= 0; i< pparticleCount ;i++)    {
                posL[i].x = rand() %10;
                posL[i].y = rand() %10;
                std::cout<<"START\n"<<i<<":"<<posL[i].x<<","<<posL[i].y<<std::endl;
            }
        }
        



};
