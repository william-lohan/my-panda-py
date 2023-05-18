#version 330

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;
uniform mat3 p3d_NormalMatrix;

// Vertex inputs
in vec4 p3d_Vertex;
in vec3 p3d_Normal;
in vec2 p3d_MultiTexCoord0;

uniform float snapScale;

// Output to fragment shader
out vec2 texcoord;

float snap(float value)
{
    // float snapScale = 10;
    return floor(value * snapScale)/snapScale;
}

void main()
{
    // jitter
    vec4 tempPos = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    tempPos.x = snap(tempPos.x);
    tempPos.z = snap(tempPos.z);

    gl_Position = tempPos;

    texcoord = p3d_MultiTexCoord0;
}
