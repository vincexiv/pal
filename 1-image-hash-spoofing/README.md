## About
This is a tool that takes an image and an arbitrary hexstring and outputs an adjusted file that displays identically to the human eye (when opened in image viewers) but has a hash that begins with the given hexstring

## Run the app
`./spoof <hex_string> <path_to_original_png_file> <path_to_altered_png_file>`

### Example
`./spoof 0x34 ./images/asta-original.png ./images/asta-altered.png`