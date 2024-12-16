- Few articles for parts of a png file <br/>
https://medium.com/@0xwan/png-structure-for-beginner-8363ce2a9f73 <br/>
https://www.w3.org/TR/PNG-Structure.html#:~:text=A%20PNG%20file%20consists%20of,discussed%20in%20the%20next%20chapter <br/>

To change its checksum to start with a particular string, randomly change parts of the image then 
get the checksum. Repeat this until the checksum matches our need; i.e, it starts with particular 
string.

In this work, I focus on the part that won't change the image, which is mostly 
metadata. I would also change the image itself by using a very small sample, e.g sampling 
like say 1% of the total number of pixels and slightly modify them (I believe the whole image 
will not look that different under this kind of modification).