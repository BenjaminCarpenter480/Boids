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
        position * prevPosL;
        position * dir;
        const float radius = 100; 
        
        float dt = 0.05 ;
    
        unsigned int particleCount;
        position* normaliseArr(position* arr,int size) {
            /*
             * Normalisation function used by opengl to display points
             */
            double maxDistX = arr[0].x;
            double maxDistY = arr[0].y; 
            for (int i = 1; i < size ; i++) {
                 if (maxDistX < arr[i].x)  {
                    maxDistX =  arr[i].x;   
                 }
                 if (maxDistY < arr[i].y)   {
                     maxDistY = arr[i].y;
                }
            }
             
            position* arrRet = new position[size];
           
            if(maxDistX>maxDistY)   {
                for (int i = 0; i < particleCount ; i++) {
                    arrRet[i].x = arr[i].x/maxDistX;
                    arrRet[i].y = arr[i].y/maxDistX;
                }
            }else    {
                for (int i = 0; i < particleCount ; i++) {
                    arrRet[i].x = arr[i].x/maxDistY;
                    arrRet[i].y = arr[i].y/maxDistY;
                }
            }
            
            return arrRet;
        }

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


        double updateMax1DMag(position test_pos, double max_mag)  {
            if(test_pos.x>max_mag)    {
                max_mag = test_pos.x;
                
            }else if(test_pos.y>max_mag)   {
                max_mag = test_pos.y ;
            }
            return max_mag;     
                
        }

        




    
    public:
        const unsigned int dimensionality = 2;
        double * getBuffer() {
            //SETUP BUFFER AND NORMALISED POSITIONS
            position * posLNorm = normalisePosArr();//GEt normalised points in allowed form [-1,1]
            double * retBuffer = new double[particleCount*dimensionality*3+dimensionality*dimensionality*2];//Buffer to return and send to gpu
            position * flatTriag = new position[particleCount*3];

            //AXES LINES POSTIONS
            retBuffer[0] = 0;
            retBuffer[1] = 0;

            retBuffer[2] = 0;
            retBuffer[3] = 1;


            retBuffer[4] = 0;
            retBuffer[5] = 0;
            
            retBuffer[6] = 1;
            retBuffer[7] = 0;

            //Setup arrow coords
            double max_1d_mag=0; 
            unsigned int j = 0;//Track position in new array/buffer where to place next 
            for (int i = 0; i < particleCount ; i++) {
                flatTriag[j].x = posL[i].x + radius*dir[i].x;
                flatTriag[j].y = posL[i].y + radius*dir[i].y;
                max_1d_mag =  updateMax1DMag(flatTriag[j],max_1d_mag);
                
                //std::cout<<flatTriag[j].x<<","<<flatTriag[j].y<<std::endl;
                j++;
                position dir_t ;
                dir_t.x = 1;
                dir_t.y =  -1*dir[i].x/dir[i].y;

                double mag = pow(pow(dir_t.x,2)+pow(dir_t.y,2),1/2);
                flatTriag[j].x = posL[i].x + (dir_t.x/mag)*radius/2;
                flatTriag[j].y = posL[i].y + (dir_t.y/mag)*radius/2;
                max_1d_mag =  updateMax1DMag(flatTriag[j],max_1d_mag);

                //std::cout<<flatTriag[j].x<<","<<flatTriag[j].y<<std::endl;
                j++;
                flatTriag[j].x = posL[i].x + dir_t.x/mag*-1;
                flatTriag[j].y = posL[i].y + dir_t.y/mag*-1;
                max_1d_mag =  updateMax1DMag(flatTriag[j],max_1d_mag);

                std::cout<<i<<":    "<<flatTriag[j-2].x<<","<<flatTriag[j-2].y<<","<<flatTriag[j-1].x<<","<<flatTriag[j-1].y<<","<<flatTriag[j].x<<","<<flatTriag[j].y<<std::endl;
                j++;
                
                //std::cin.get();    
            }

            std::cout << "-------------"<<max_1d_mag<<"---------------\n";
            // flatTriag = normaliseArr(flatTriag,particleCount*3);
            //max_1d_mag = 10000;
            //Must flatten 2d array of positions
            //MUST BE NORMALISED SOMWHERE BELOW
            unsigned int c = 8;//Track position in new array/buffer where to place next 
            for (int i = 0; i < particleCount*3 ; i++) {
                retBuffer[c] = flatTriag[i].x/max_1d_mag;
               // std::cout<<retBuffer[c]<<",";
                c++;
                retBuffer[c] = flatTriag[i].y/max_1d_mag;
               // std::cout<<retBuffer[c]<<std::endl;
                c++;
            }
        
        return retBuffer;
        }

        unsigned int findFurthestNeighbour(unsigned int index)    {
            double maxDist = sqrt(pow(posL[0].x,2)+pow(posL[0].y,2)); 
            unsigned int nnIndex = 0;
            for (int i = 1; i < particleCount ; i++) {
                if (index != i) {
                    double currentDist = sqrt(pow(posL[i].x,2)+pow(posL[i].y,2))  ; 
                    if (maxDist < currentDist)  {
                        maxDist = currentDist;
                        nnIndex = i;
                    }
                }
            }
            return nnIndex;
        }


        unsigned int findNearestNeighbour(unsigned int index)    {
            double minDist = 1e32; //sqrt(pow(posL[0].x,2)+pow(posL[0].y,2)); 
            unsigned int nnIndex = 0;
            for (int i = 0; i < particleCount ; i++) {
                if (index != i) {
                    double currentDist = sqrt(pow(posL[i].x-posL[index].x,2)+pow(posL[i].y-posL[index].y,2))  ; 
                    if (minDist > currentDist)  {
                        minDist = currentDist;
                        nnIndex = i;
                    }
                }
            }
            return nnIndex;
        }

        position moveAwayDir(int xS, int yS, int xT, int yT)    {
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
            position dir_t; 
            dir_t.x= ((rand()-RAND_MAX/2)%RAND_MAX/(double)RAND_MAX);
             
            dir_t.y= ((rand()-RAND_MAX/2)%RAND_MAX/(double)RAND_MAX);

            return dir_t;
        }

        position randAdjust(unsigned i)   {
            //Makes a slight adjustment to the direction travelled rather than totally changing position
            position dir_t;
            dir_t.x = (posL[i].x - prevPosL[i].x)+(rand()-RAND_MAX/2)%RAND_MAX/(double)RAND_MAX;
            dir_t.y = (posL[i].y - prevPosL[i].y)+(rand()-RAND_MAX/2)%RAND_MAX/(double)RAND_MAX;
            double mag = sqrt(pow(dir_t.x,2)+pow(dir_t.y,2));
            dir_t.x = dir_t.x/mag;
            dir_t.y = dir_t.y/mag;
            return dir_t;
        }
        

        void timeStep() {//Position updater function
            std::cout<<"Timestep\n";
            for (int i= 0; i<particleCount/*sizeof(*posL)/sizeof(*position)*/;i++)    {
               
                //Update the previous position 
                prevPosL[i].x = posL[i].x;
                prevPosL[i].y = posL[i].y;
                

                unsigned int nnIndex = findNearestNeighbour(i);
                //position dir_t;
                //= moveAwaydir_t(posL[i].x,posL[i].y,posL[nnIndex].x,posL[nnIndex].y);
                if(distBetween(posL[i],posL[nnIndex])<100)    {
                    dir[i] = moveAwayDir(posL[i],posL[nnIndex]);
                }else   { 
                    //dir_t = randWalk(); 
                    dir[i] = randAdjust(i);
                }

                
                posL[i].x = posL[i].x +dt*dir[i].x;
                posL[i].y = posL[i].y +dt*dir[i].y;
                
                 

                //std::cout<<"P:"<<i<<std::endl;
                //std::cout<<"dr:"<<dir.x<<","<<dir.y<<std::endl; 
                //std::cout<<"Positions:"<<posL[i].x<<","<<posL[i].y<<std::endl;
            }
         
                
        }


        double * updatePositions()  {
            timeStep();
            return getBuffer();
        }



        testSim(unsigned int pparticleCount,double pdt,int k) {
            dt = pdt;
            particleCount = pparticleCount;
            posL = new position[pparticleCount];
            prevPosL = new position[pparticleCount];
            dir = new position[pparticleCount];
            for (int i= 0; i< pparticleCount ;i++)    {
                //Setup initial posiitons and dir_tections
                posL[i].x = (rand()-RAND_MAX/2)%k;
                posL[i].y = (rand()-RAND_MAX/2)%k;
                prevPosL[i].x = 0;
                prevPosL[i].y = 0;

                //std::cout<<"START\n"<<i<<":"<<posL[i].x<<","<<posL[i].y<<std::endl;
            }
        }
        



};
