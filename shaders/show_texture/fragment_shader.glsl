#version 130

in vec2 fragment_texCoord;	// The fragment texture coordinates

out vec4 final_color; 		// The only output is the fragment colour

uniform sampler2D sampler;	// The cube map texture

void main(void)
{
	// Sample from the cube map texture
	final_color = texture(sampler, fragment_texCoord);
}
