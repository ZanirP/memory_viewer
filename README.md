# Memory Viewer

Memory Viewer is a tool designed to help developers visualize and analyze memory usage in their ARMv8 code. This tool provides a graphical interface to inspect memory allocations, deallocations, and overall memory consumption. (at least it will when it is done)
I am planning on deploying soon! Just as a MVP I will work on updates from time to time! 

## Next steps 
 - Store and Load aren't working so I think that has to do with me not fully understanding what is suppose to occur - going to do research - and fix those files
 - Front-end will need lots of work to make it look nice, right now is just MVP
 - UnitTests need to be MASSIVELY improved - i.e. needs to test overflow, (for everything), and test all other funtionalities of ARM (edge cases and things ARM does in a weird way)

## Features

- Visual representation of memory usage
- Track memory allocations and deallocations
- Analyze memory consumption over time
- Export memory usage reports

## Installation

To install Memory Viewer, follow these steps:

1. Clone the repository:
	```sh
	git clone https://github.com/yourusername/memory_viewer.git
	```
2. Navigate to the project directory:
	```sh
	cd memory_viewer
	```
3. Install the required dependencies:
	```sh
	npm install
	```

## Usage

To start using Memory Viewer, run the following command:
```sh
npm start
```

Open your web browser and navigate to `http://localhost:3000` to access the Memory Viewer interface.

## Contributing

We welcome contributions to Memory Viewer! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or inquiries, please contact us at [email@example.com](mailto:email@example.com).
