# 🏁 Sort Race – Sorting Algorithm Battle Arena

A Python-based visual sorting simulator that compares **Bubble Sort, Insertion Sort, Merge Sort, and Quick Sort** in a real-time race using animated bars.

Each algorithm sorts the same input data in its own lane. Watch the algorithms work step by step and compare their performance using comparisons, writes, and total steps.

## ✨ Features

- 🏎️ **Four Sorting Algorithms:** Bubble Sort, Insertion Sort, Merge Sort, and Quick Sort.
- 📊 **Real-Time Visualization:** Watch the sorting process through animated bar charts.
- 📈 **Performance Statistics:** Track comparisons, writes, and steps for each algorithm.
- 🎲 **Multiple Data Types:** Generate random, nearly sorted, reversed, or few-unique-value datasets.
- ✍️ **Custom Input:** Enter your own numbers to test the algorithms.
- ⚡ **Adjustable Speed:** Control the animation speed.
- 🏆 **Race Results:** See which algorithm finishes first and compare the number of steps required.
- 🎨 **Color-Coded Lanes:** Each algorithm has a different color, with highlighted bars showing the values currently being processed.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **GUI:** Tkinter
- **Libraries:** `math`, `random`, `re`, `tkinter`, and `tkinter.ttk`

## 📋 Sorting Algorithms

| Algorithm | Average Time Complexity | Worst-Case Time Complexity |
|---|---|---|
| Bubble Sort | O(n²) | O(n²) |
| Insertion Sort | O(n²) | O(n²) |
| Merge Sort | O(n log n) | O(n log n) |
| Quick Sort | O(n log n) | O(n²) |

*Note: Quick Sort uses a middle-position pivot selection in this project. Its worst-case complexity remains O(n²).*

## 🚀 Getting Started

### Prerequisites

- Python 3 installed on your computer.
- Tkinter available in your Python installation.

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

Replace `YOUR-USERNAME` and `YOUR-REPOSITORY` with your GitHub username and repository name.

**2. Open the project folder**

```bash
cd YOUR-REPOSITORY
```

**3. Run the application**

```bash
python sort_race_.py
```

If your file has a different name, replace `sort_race_.py` with the correct filename.

## 🎮 How to Use

1. Launch the application.
2. Select a dataset type from the **Data** dropdown.
3. Adjust the array size using the size slider.
4. Choose your preferred animation speed.
5. For custom input, select **My own numbers** and enter at least 2 numbers, separated by commas, spaces, or semicolons.
6. Click **New data** to generate or reshuffle the dataset.
7. Click **Start race** to begin the sorting animation.
8. Compare the algorithms using their statistics and final race results.

## 📊 Performance Metrics

The application displays three main statistics for each algorithm:

- **Comparisons:** Number of comparisons performed between values.
- **Writes:** Number of array write operations counted by the implementation.
- **Steps:** Number of animation operations processed by the algorithm.

The race uses a shared animation tick to advance each unfinished algorithm, making the sorting process easy to observe.

## 🎯 Project Objective

The main objective of this project is to demonstrate how different sorting algorithms work and how their performance changes with different input datasets.

It provides a visual and interactive way for students and beginners to understand sorting algorithms, time complexity, and algorithmic performance.

## 🔮 Future Improvements

- Add Heap Sort and Selection Sort.
- Display execution time for each algorithm.
- Add pause, resume, and reset controls.
- Export performance statistics to CSV.
- Create performance comparison charts for different array sizes.

## 👨‍💻 Author

**Riddhesh Gavad**

## 📄 License

This project is available for educational and learning purposes. Add a license file to the repository if you want to specify formal reuse and distribution terms.
