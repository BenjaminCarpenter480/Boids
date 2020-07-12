/*
 *
 * TODO: RENAME position struct to vector
 * UPDATE BASE MOVEMENT FROM RANDOM WALK TO ONLY A SLIGHT CHANGE FROM THE PREVIOUS DIRECTION 
 */


#include <cmath>
#include <chrono>
#include <thread>
class testSim   {
    private:
        struct position {
            double x;
            double y;
        };
        position * posL;
        float dt = 0.05 ;
    
        unsigned int particleCount;
        
        position* normalisePosArr() {
            /*
             * Normalisation function used by opengl to display points
             */
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
            }else    {
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
            position * posLNorm = normalisePosArr();//GEt normalised points in allowed form [-1,1]
            double * retBuffer = new double[particleCount*dimensionality];//Buffer to return and send to gpu
           
            //Must flatten 2d array 
            unsigned int c = 0;//Track position in new array/buffer where to place next 
            for (int i = 0; i < particleCount ; i++) {
                retBuffer[c] = posLNorm[i].x;
                c++;
                retBuffer[c] = posLNorm[i].y;
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
        position moveAwayDir(position self, position posAwayFrom)  {
            return moveAwayDir(self.x,self.y,posAwayFrom.x,posAwayFrom.y);
        }


        double distBetween(position A, position B)  {
            return sqrt(pow(A.x-B.x,2)+pow(A.y-B.y,2));
        }
        

        position randWalk() {
            position dir; 
            dir.x= ((rand()-RAND_MAX/2)%RAND_MAX/(double)RAND_MAX);
             
            dir.y= ((rand()-RAND_MAX/2)%RAND_MAX/(double)RAND_MAX);

            return dir;
        }

        
        void timeStep() {//Position updater function
            std::cout<<"Timestep\n";
            for (int i= 0; i<particleCount/*sizeof(*posL)/sizeof(*position)*/;i++)    {
                unsigned int nnIndex = findNearestNeighbour(i);
                position dir;
                //= moveAwayDir(posL[i].x,posL[i].y,posL[nnIndex].x,posL[nnIndex].y);
                if(distBetween(posL[i],posL[nnIndex])<100)    {
                    dir = moveAwayDir(posL[i],posL[nnIndex]);
                }else   { 
                    dir = randWalk(); 
                }

                

                posL[i].x = posL[i].x +dt*dir.x;
                posL[i].y = posL[i].y +dt*dir.y;
                
                 

                std::cout<<"P:"<<i<<std::endl;
                std::cout<<"dr:"<<dir.x<<","<<dir.y<<std::endl; 
                std::cout<<"Positions:"<<posL[i].x<<","<<posL[i].y<<std::endl;
                
            }
         
        }


        double * updatePositions()  {
            timeStep();
            return getPosBuffer();
        }



        testSim(unsigned int pparticleCount,double pdt,int k) {
            dt = pdt;
            particleCount = pparticleCount;
            posL = new position[pparticleCount];
            for (int i= 0; i< pparticleCount ;i++)    {
                posL[i].x = (rand()-RAND_MAX/2)%k;
                posL[i].y = (rand()-RAND_MAX/2)%k;
                std::cout<<"START\n"<<i<<":"<<posL[i].x<<","<<posL[i].y<<std::endl;
            }
        }
        



};
