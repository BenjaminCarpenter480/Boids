#include <iostream>


#include "GL/glew.h"

#include "GL/glut.h"

#include "GLFW/glfw3.h"

#include <functional>

#include <fstream>
#include <string>
#include <sstream>
class GLWrap    {
    public:
    //private:
        unsigned int particleCount ;
        unsigned int dimensionCount;
        //TYPE AS VARIABLE CURRENTLY JUST DOUBLE
        unsigned int shader;
    //#define GL_GLEXT_PROTOTYPES
        struct ShaderSourceCode {
            std::string VertexSource;
            std::string FragmentSource;
        };
        GLFWwindow* window;

     
        static ShaderSourceCode ParseShader(const std::string& filepath )   {
            /* Parse shader files */
            std::ifstream stream(filepath); //Open file
            
            enum class ShaderType
            {
                NONE = -1 , VERTEX = 0 , FRAGMENT = 1
            };
            
            std::string line;
            std::stringstream ss[2];
            ShaderType type = ShaderType::NONE;
            
            while(std::getline(stream,line)) {
                if(line.find("#shader") != std::string::npos)   {
                    if(line.find("fragment") != std::string::npos)
                        //Set mode fragmenta
                        type = ShaderType::FRAGMENT;
                    else if (line.find("vertex") != std::string::npos)
                        //set mode vertex
                        type = ShaderType::VERTEX;
                }
                else    { //Otherwise we add to the shader string
                    ss[(int)type] << line << "\n";
                }
            }
            return {ss[0].str(),ss[1].str()};
            
        
        }
        
        static unsigned int CompileShader(unsigned int type, const std::string& sourceCode) {
            unsigned int id = glCreateShader(type);
            const char* srcCode = sourceCode.c_str();
            glShaderSource(id,1,&srcCode,nullptr);
            glCompileShader(id);
        
            //Some error handelling code
            int result;
            glGetShaderiv(id,GL_COMPILE_STATUS,&result);
            if(result==GL_FALSE)    {
        
                std::cout <<"FAILED TO COMPILE shader!" << std::endl;
                int length;
                glGetShaderiv(id,GL_INFO_LOG_LENGTH,&length);
                char* message = (char*) alloca(length*sizeof(char));
                glGetShaderInfoLog(id,length,&length,message);
                std::cout<< message <<std::endl ; 
                glDeleteShader(id);
                return 0;
            }
            return id;
            
        }
        
        static unsigned int CreateShader(const std::string& vertexShader,
                                         const std::string& fragmentShader) {
            unsigned int program = glCreateProgram();
            unsigned int vs = CompileShader(GL_VERTEX_SHADER, vertexShader);
            unsigned int fs = CompileShader(GL_FRAGMENT_SHADER, fragmentShader);
            
            glAttachShader(program, vs);
            glAttachShader(program, fs);
            glLinkProgram(program);
            glValidateProgram(program);
            
            glDeleteShader(vs);
            glDeleteShader(fs);
        
            return program;
            }
        
        
        int setupWindow()    {
            //GLFWwindow* lwindow;
            if (!glfwInit())    {
                std::cout<<"GLFW Error\n";
                return -1;
            }
              
            //Create window & OpenGL context
            window = glfwCreateWindow(640,480,"WINDOW NAME", NULL, NULL);
           
            if (!window)    {
                glfwTerminate();
                std::cout<<"GLFW Error\n";
                return -1;
            }
           
            //Make windows context current
            glfwMakeContextCurrent(window);
        
            if (glewInit() != GLEW_OK)  {
                std::cout<<"GLEW Error\n";
                return -1;
            }
            //window= window;
            return 0;
        }
    //public:
        unsigned int buffer; //Address of buffer
        unsigned int axesBuffer;
        //GLFWwindow* window;
        
        GLWrap(unsigned int p_particleCount, unsigned int p_dimensionCount)  {
                       
            particleCount = p_particleCount;
            dimensionCount = p_dimensionCount;
            setupWindow(); //Maybe should deal with -1 reutrns and stuff
        
            glfwSwapInterval(0); //NUMBER OF VSYNCS TO DO 
            setupBuffer(particleCount,dimensionCount);
            //setupParticles(particleCount,dimensionCount);
            //setupAxes();
            ShaderSourceCode source =ParseShader("shader.shader");
             
            shader = CreateShader(source.VertexSource, source.FragmentSource);
            glUseProgram(shader);




            
        };
        void setupBuffer(unsigned int p_particleCount, unsigned int p_dimensionCount)  {
 
            
            glGenBuffers(1,&buffer); //Gen single buffer with addr of buffer
            
            

            glBindBuffer(GL_ARRAY_BUFFER, buffer); //Select a buffer and tell some info on the buffer
            
            //Spec data of buffer
            glBufferData(GL_ARRAY_BUFFER,
                         (dimensionCount)*(dimensionCount)*sizeof(double)
                             +particleCount*dimensionCount*sizeof(double),
                         NULL,
                         GL_STREAM_DRAW);

            /*Define the buffer size, items and type of accesses for the buffer e.g. static where 
             * data mod once, accessed many and draw implying usage as drawing 'instruction'
             */

            //glBufferSubData(GL_ARRAY_BUFFER,0,particleCount*dimensionCount*sizeof(float),pos);
        
            glEnableVertexAttribArray(0);  //ENable below attrib
        
            
            glVertexAttribPointer(0,2,GL_DOUBLE,GL_FALSE,sizeof(double)*dimensionCount,0); 
            //Define the attrib (2D positions)
    
            //glEnableVertexAttribArray(1);

            glBindBuffer(GL_ARRAY_BUFFER,0);  
            
        }


        
        
        int getExitAnimation() {
        /*
         *  Exit window check function
         */
            return glfwWindowShouldClose(window);
        }

        int exitWindow()    {
        
            glDeleteProgram(shader);
            return 0;
        }

        void draw(double* dataBuffer)   {
            //points BUFFER UPDATUNG (SHOULD REALLY BE A LOOP FOR MULTIPLE UPDATES
            glBufferData(GL_ARRAY_BUFFER,
                         (dimensionCount)*(dimensionCount)*sizeof(double)
                             +particleCount*dimensionCount*sizeof(double),
                         NULL,
                         GL_STREAM_DRAW);
       

            glBufferSubData(GL_ARRAY_BUFFER,
                    0,
                    (dimensionCount)*(dimensionCount)*sizeof(double)
                             +particleCount*dimensionCount*sizeof(double),

                    dataBuffer);
            
            
            
            //SEND points buffer DATA TO GPU i.e. update buffer (I THINK) 
            glBindBuffer(GL_ARRAY_BUFFER, buffer); //select a buffer and tell some info on the buffer
            //DRAW
            //shape,start index,count of items.
            //std::cout<<retBuffer[c];
            glDrawArrays(GL_LINES,0,4);//dimensionCount);        !!!!?????Need sizeof ?????
            
            //std::cout<<"------------\n"<<dataBuffer[4]<<"-------------\n";
            //std::cin.get();
            glDrawArrays(GL_TRIANGLES,4,particleCount);
 
        }



   

        
        int updateScreen()  {//double* pointPos)   {
            //WINDOW HANDLING:
             

            //WINDOW HANDLING: Front & back buffer swap
            glfwSwapBuffers(window);
            //WINDOW HANDLING: RESIZE WINDOW
            int width, height;
        
            glfwGetWindowSize(window, &width,&height);
        
            glViewport(0,0,width,height);
        
            //WINDOW HANDLING: Poll for and process any events
            glfwPollEvents();
            //std::cin.get(); 
        
            return 0;
        }
        
    void screenClear()  {    
        glClear(GL_COLOR_BUFFER_BIT);
    }
        

};
