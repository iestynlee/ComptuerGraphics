# version 130 // required to use OpenGL core standard

// === 'in' attributes are passed on from the vertex shader's 'out' attributes, and interpolated for each fragment
in vec2 fragment_texCoord;

// === 'out' attributes are the output image, usually only one for the colour of each pixel
out vec4 final_color;

// Texture samplers
uniform sampler2D textureObject; // first texture object

///=== main shader code
void main() {
    // Sample from the texture
    vec4 texval = vec4(1.0f);

    // Sample from the texture
    texval = texture2D(textureObject, fragment_texCoord);

    final_color = texval;
}


