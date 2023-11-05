# The CS917 Programming Coursework

## some of my thoughts

In this coursework, I tried to use all of my knowledge of Python and general coding concepts
to create each of the 4 parts.

However, I found that there were some requirements in the coursework not quite clear.
For example, it just mentioned that TA will test our code by importing the function from its module,
not specify the input type of `data`, which is a bit confusing.

In my personal opinion, I would like to follow the clean code principle,
so my strategy of this kind of real-world problem is to create a clear Model structure with its DTO (Data Transfer
Object)
to read the data from the csv file.

But if the coursework asks us to read the file every time when the function is called,
I might think about how to reduce the duplicated file reading code.

Additionally, I tried to use the `unittest` module to test my code,
which is better than test by just seeing the output.

### So...What ?

Maybe the code will be tested by just importing the function from the module,
but I hope that you can understand my intention of the code, and run the code directly
by the follow command:

```bash
# If you want to run the part a
python3 main.py a
```

This will trigger all the test function of parta, and print the result of each test.

### Conclusion

Generally, I think this coursework is a good practice for us to practice Python.

However, it is not a good idea to bring the expected solution into real-world cases.

I cannot always say that my solution is the best, but as a CS student(NOT a Mathmatics student),
I hope to see a more practical problem in the future,
meanwhile, I also hope people in the CS of the University of Warwick can put more effort into the teaching of CS,
instead of pure Mathmatics.

Good luck to my grade :)
