#include <iostream>


#include "GL/glew.h"

#include "GL/glut.h"

#include "GLFW/glfw3.h"


#include <fstream>
#include <string>
#include <sstream>


//#define GL_GLEXT_PROTOTYPES
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


int main()
{
    
    unsigned int ParticlesCount = 20;
    unsigned int MaxParticles = ParticlesCount;
    
    
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
    
    float pos[] = {-0.5f,-0.5f,0.0f,
                  0.0f, 0.5f,0.0f,
                  0.5f,-0.5f,0.0f,
                  0.5f,0.0,0.0f};


    float vertex_pos[] = {-0.5f,-0.5f,0.0f,
                  0.0f, 0.5f,0.0f,
                  0.5f,-0.5f,0.0f,
                  0.5f,0.0,0.0f};



    unsigned int spaceBuffer; //Address of buffer
    glGenBuffers(1,&spaceBuffer); //Gen single buffer with addr of buffer
    
    glBindBuffer(GL_ARRAY_BUFFER, spaceBuffer); //Select a buffer and tell some info on the buffer


    //Spec data of bufferglBufferData(GL_ARRAY_BUFFER,6*sizeof(float),NULL,GL_DYNAMIC_DRAW);
    glBufferData(GL_ARRAY_BUFFER,sizeof(vertex_pos),vertex_pos,GL_STATIC_DRAW);
     
    /* once, accessed many and draw implying usage as drawing 'instruction'
     */

    unsigned int posBuffer;
    glGenBuffers(1,&posBuffer);
    glBindBuffer(GL_ARRAY_BUFFER, posBuffer);
    glBufferData(GL_ARRAY_BUFFER,MaxParticles*4*sizeof(GLfloat),NULL,GL_STREAM_DRAW);


    unsigned int colBuffer;
    glGenBuffers(1,&colBuffer);
    glBindBuffer(GL_ARRAY_BUFFER,colBuffer);
    glBufferData(GL_ARRAY_BUFFER,MaxParticles*4*sizeof(GLubyte),NULL,GL_STREAM_DRAW);
    

    glEnableVertexAttribArray(0);  //ENable below attrib

    glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,sizeof(float)*3,0); //Define the attrib
    
        
    ShaderSourceCode source =ParseShader("shader.shader");
    


    unsigned int shader = CreateShader(source.VertexSource, source.FragmentSource);
    glUseProgram(shader);

    glBindBuffer(GL_ARRAY_BUFFER,0);  
    //lookup exactly what this is doing but think just selects or buffer defined above
    
    glVertexAttribDivisor(0, 0); // particles vertices : always reuse the same 4 vertices -> 0
    glVertexAttribDivisor(1, 1); // positions : one per quad (its center) -> 1
    glVertexAttribDivisor(2, 1); // color : one per quad -> 1

    glDrawArraysInstanced(GL_TRIANGLE_STRIP, 0, 3, ParticlesCount);


    //Whilst window opened
    while(!glfwWindowShouldClose(window))
    {
        //WINDOW HANDLING:
        glClear(GL_COLOR_BUFFER_BIT);

        glDrawArraysInstanced(GL_POINTS,0,3,ParticlesCount);//shape,start index,count of items.


        //glBufferData(GL_ARRAY_BUFFER,6*sizeof(float),pos,GL_DYNAMIC_DRAW);

        pos[0] =  rand();
        pos[1] = rand();        
        pos[2] = rand();            
        pos[3] = rand();
        pos[4] = rand();
        pos[5] = rand();
        
        glBindBuffer(GL_ARRAY_BUFFER, posBuffer);
        glBufferData(GL_ARRAY_BUFFER,MaxParticles*4*sizeof(GLfloat),NULL,GL_STREAM_DRAW);
        glBufferSubData(GL_ARRAY_BUFFER,0,ParticlesCount*sizeof(GLfloat)*4,pos);
       
        glDrawArraysInstanced(GL_POINTS,0,3,ParticlesCount);
        /*
        glBindBuffer(GL_ARRAY_BUFFER,colBuffer);
        glBufferData(GL_ARRAY_BUFFER,MaxParticles*4*sizeof(GLubyte),NULL,GL_STREAM_DRAW));
        */

        //glBufferData(GL_ARRAY_BUFFER,6*sizeof(float),NULL,GL_DYNAMIC_DRAW);
        //glBufferSubData(GL_ARRAY_BUFFER,0,6*sizeof(float),pos);

        

        //WINDOW HANDLING: Front & back buffer swap
        glfwSwapBuffers(window);

        //WINDOW HANDLING: Poll for and process any events
        glfwPollEvents();

    }
    glDeleteProgram(shader);

    return 0;
}
//
