#include "GL/glew.h"

#include "GL/glut.h"

#include "GLFW/glfw3.h"


#include <fstream>
#include <string>
#include <sstream>




class GLGraph   {
    public:
        GLGraph()   {
            GLFWwindow* window;
            if (!glfwInit())    {
                return -1;
            }
              
            //Create window & OpenGL context
            window = glfwCreateWindow(640,480,"Hello World", NULL, NULL);
   
            if (!window)    {
                glfwTerminate();
                return -1;
            }
   
            //Make windows context current
            glfwMakeContextCurrent(window);

            if (glewInit() != GLEW_OK)  {
                std::cout<<"ERROR!\n";
                return -1;
            }
            
            float pos[] = {-0.5f,-0.5f,
                          0.0f, 0.5f,
                          0.5f,-0.5f};


            unsigned int buffer; //Address of buffer
            glGenBuffers(1,&buffer); //Gen single buffer with addr of buffer
            
            glBindBuffer(GL_ARRAY_BUFFER, buffer); //Select a buffer and tell some info on the buffer


            //Spec data of buffer
            glBufferData(GL_ARRAY_BUFFER,6*sizeof(float),pos,GL_STATIC_DRAW);
            /*Define the buffer size, items and type of accesses for the buffer e.g. static where data mod
             * once, accessed many and draw implying usage as drawing 'instruction'
             */

            glEnableVertexAttribArray(0);  //ENable below attrib

            glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,sizeof(float)*2,0); //Define the attrib
            
                
            ShaderSourceCode source =ParseShader("shader.shader");
            


            unsigned int shader = CreateShader(source.VertexSource, source.FragmentSource);
            glUseProgram(shader);

            glBindBuffer(GL_ARRAY_BUFFER,0);  
            //lookup exactly what this is doing but think just selects or buffer defined above

            //Whilst window opened
            while(!glfwWindowShouldClose(window))
            {
                //WINDOW HANDLING:
                glClear(GL_COLOR_BUFFER_BIT);

                glDrawArrays(GL_TRIANGLES,0,3);//shape,start index,count of items.

                
                
                //WINDOW HANDLING: Front & back buffer swap
                glfwSwapBuffers(window);

                //WINDOW HANDLING: Poll for and process any events
                glfwPollEvents();

            }
            glDeleteProgram(shader);

            return 0;

        }
       ////////////////////////////////////////////////////////////////////////// 
        struct ShaderSourceCode {
            std::string VertexSource;
            std::string FragmentSource;
        };


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
        
        static unsigned int CreateShader(const std::string& vertexShader, const std::string& fragmentShader)    {
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
    
    private:
}
