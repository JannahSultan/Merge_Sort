"""
Merge Sort Visualizer - Interactive Tool
This application demonstrates the merge sort 
algorithm with step by step visualization
Author: Jannah Sultan
Date: 10th December 2025
"""
import random
import gradio as gr
import plotly.graph_objects as go

# --------------------------------------------------------------------------------------------------
# GLOBAL CONSTANTS
# --------------------------------------------------------------------------------------------------

MAX_ARRAY_LENGTH = 50
MIN_ARRAY_LENGTH = 1
SMALL_ARRAY_MAX_VALUE = 30
LARGE_ARRAY_MAX_VALUE = 100

# --------------------------------------------------------------------------------------------------
# GLOBAL STATE
# --------------------------------------------------------------------------------------------------

unsorted_array = [] # stores the current unsorted array being worked on

# --------------------------------------------------------------------------------------------------
# ARRAY GENERATION FUNCTION
# --------------------------------------------------------------------------------------------------

def generate_random_array(length_input):
    """
    This function validates the user's input, generates an array of random 
    integers, and updates the UI state to enable the sorting button.
    
    Args:
        length_input (str or int):The desired length of the array from the user input
    Returns:
        tuple: A 4-element tuple containing:
               - str or list: an error message or the generated array
               - gr.update: a button state update for the 'generate' button
               - gr.update: a textbox state update for the length input
               - gr.update: a button state update for the 'start sorting' button
               
    Raises:
        ValueError: If input cannot be converted to integer
    """
    
    unsorted_array.clear() #clear any previously generated array

    # VALIDATION 1: Check for empty input
    if not length_input or str(length_input).strip() == "":
        return (
            "⚠️ Please enter a number!", 
            gr.update(), #keep generate button as-is
            gr.update(), #keep input textbox as-is
            gr.update()  #keep start button as-is
        )

    # VALIDATION 2: Try to convert input to integer
    try:
        length_input_txtbox = int(length_input)
    except ValueError:
        return (
            "❌ Please enter a valid integer!",
            gr.update(), #generate button
            gr.update(), #length input
            gr.update(), #start sorting button
        )
        
    # VALIDATION 3: Check if length input is positive
    if length_input_txtbox <= 0:
        return (
            "❌ Array length must be positive!", 
            gr.update(), #generate button
            gr.update(), #length input
            gr.update(), #start sorting button
        )
            
    # VALIDATION 4: Check if length input exceeds maximum
    if length_input_txtbox > MAX_ARRAY_LENGTH:
        return (
            f"❌ Array length cannot exceed {MAX_ARRAY_LENGTH}!",
            gr.update(), #generate button
            gr.update(), #length input
            gr.update(), #start sorting button
        )

    # Generate random array based on input (for array size)
    for _ in range(length_input_txtbox):
        if length_input_txtbox < 50: # smaller arrays get smaller values for better visualization
            max_value = SMALL_ARRAY_MAX_VALUE
        else:
            max_value = LARGE_ARRAY_MAX_VALUE
        unsorted_array.append(random.randint(1, max_value))

    # Return the array and update UI states
    return (
        unsorted_array,                  # display the generated array in the array display output textbox
        gr.update(interactive=False),    # disable generate_btn
        gr.update(interactive=False),    # disable length textbox
        gr.update(interactive=True),     # enable start_sorting_btn
    )

# --------------------------------------------------------------------------------------------------
# MERGE SORT ALGORITHM WITH STEP-BY-STEP VISUALIZATION
# --------------------------------------------------------------------------------------------------

def visualize_merge_sort_steps(arr):
    """
    This generator function implements merge sort while yielding visualization 
    data at each significant step (such as splitting, comparing, and merging).
    
    Args:
        arr (list): List of integers to sort
        
    Yields:
        tuple: A 4-element tuple for each step:
            - str: Step type (currently always "display")
            - str: Human-readable message explaining current step
            - list: Current state of the full array
            - tuple: (start_index, end_index) indicating highlighted section
    Returns:
        list: The fully sorted array (returned via StopIteration)
    """
    
    full_array = arr.copy() # create a copy of the array to track changes throughout sorting

    def sort(arr, offset=0, counter=0):
        """
        This is the main recursive function that divides the array into halves,
        sorts each half, and then merges them back together.
        
        Args:
            arr (list): The sub-array to sort
            offset (int): Starting index of this sub-array in the full array
            counter (int): Current recursion depth (for messaging personalization)
            
        Yields:
            tuple: Visualization data for each step
            
        Returns:
            list: The sorted sub-array
        """

    # BASE CASE: Arrays with 0 or 1 element are already sorted
        if len(arr) < 2:
            yield (
                "display",
                "✨ There is only 1 element in this half, so it's already sorted and perfect!",
                full_array,
                (offset, offset + len(arr) - 1),
            )
            return arr

    # DIVIDE STEP: Split array into two halves
        mid = len(arr) // 2   # Find the middle index
        left = arr[:mid]      # Left half (start to middle)
        right = arr[mid:]     # Right half (middle to end)

        # Generate descriptive text for the split
        split_text = "next " if counter != 0 else "" #if splitting second half, add "next" to existing sentence for better UX
        yield (
            "display",
            f"🔪 CHOP! Splitting the {split_text}array in half...\n"
            f"        📦 Left half consists of: {left}\n"
            f"        📦 Right half consists of: {right}",
            full_array,
            (offset, offset + len(arr) - 1), #highlight the section being split
        )

    # CONQUER STEP: Recursively sort both halves by repeatedly splitting them again until base case is reached
        counter += 1
        left_sorted = yield from sort(left, offset, counter)
        right_sorted = yield from sort(right, offset + mid, counter)

    # COMBINE STEP: Merge the two sorted halves
        result = yield from merge(left_sorted, right_sorted, offset)

        # Update the full array with the merged result
        for i, val in enumerate(result):
            full_array[offset + i] = val
            
        return result

    def merge(left, right, offset):
        """
        This function takes two sorted sub-arrays and combines them into 
        a single sorted array by comparing elements from each side.
        Args:
            left (list): First sorted sub-array
            right (list): Second sorted sub-array
            offset (int): Starting position in the full array
            
        Yields:
            tuple: Visualization data showing the merge process
            
        Returns:
            list: The merged and sorted array
        """
        
        result = [] # will hold the merged, sorted array
        left_idx = right_idx = 0   # pointers for the left and right arrays respectively

        comparison_text = "Based on the comparison, "

     # MERGE PROCESS: Compare elements from left and right arrays
        while left_idx < len(left) and right_idx < len(right):
            # compare current elements from both arrays
            if left[left_idx] <= right[right_idx]:
                # if left element is smaller or equal to right, add it to result
                result.append(left[left_idx])
                comparison_text += (
                    f"\n Comparing {left[left_idx]} and {right[right_idx]}, "
                    f"I added {left[left_idx]} from left half, "
                )
                left_idx += 1
            else:
                #  if right element is smaller, add it to result
                result.append(right[right_idx])
                comparison_text += (
                    f"\n Comparing {left[left_idx]} and {right[right_idx]}, "
                    f"I added {right[right_idx]} from right half, "
                )
                right_idx += 1
                
    #  CLEANUP: Add any remaining elements in the left and right arrays
        result.extend(left[left_idx:])
        result.extend(right[right_idx:])

        comparison_text += (
            f"(all to the start of the sorted array) and added the remaining at the end "
            f"so that the final array for this half is {result}"
        )

        #  Yeild the merge step visualization
        yield (
            "display",
            f"🤔 Comparing and merging left: {left} and right: {right}...\n{comparison_text}",
            full_array,
            (offset, offset + len(left) + len(right) - 1),
        )

        return result

    #  Start the sorting process from the root
    yield from sort(full_array, 0)
    return full_array

#  --------------------------------------------------------------------------------------------------
#  VISUALIZATION (BAR PLOT) FUNCTION
#  --------------------------------------------------------------------------------------------------

def create_bar_plot(arr, highlight_range=None, finished=False):
    """
    This function generates a Plotly bar chart where different sections
    can be highlighted with different colors to show the sorting process.
    
    Args:
        arr (list): The array to visualize
        highlight_range (tuple, optional): (start, end) indices to highlight
        finished (bool): Whether sorting is complete
        
    Returns:
        plotly.graph_objects.Figure: The configured bar chart
    """

   #  Determine colors for each bar based on highlighting 
    if highlight_range:
        start, end = highlight_range
        mid = start + (end - start + 1) // 2 #  Calculate midpoint
        
        colors = [] 
        hover_labels = []

        #  Assign colors based on position relative to highlighted range
        for i in range(len(arr)):
            if start == mid and mid == end and start == i:
                #  single element being examined
                colors.append("#FF8000")  # Orange (for single)
                hover_labels.append("")
            elif start <= i < mid:
                # left half of split
                colors.append("#FF6B6B")  # Red (for left half)
                hover_labels.append("left")
            elif mid <= i <= end:
                # right half of split
                colors.append("#FFD93D")  # Yellow (for right half)
                hover_labels.append("right")
            else:
                # not currently involved in operation
                colors.append("#8C8C8C")  # Grey (for non-highlighted)
                hover_labels.append("none")
    else:
        # No highlighting - use default colour
        hover_labels = ["sorted" if finished else "unsorted"] * len(arr)
        colors = ["#4ECDC4"] * len(arr) #Teal (for unrelated)

    # Create the bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                x=list(range(len(arr))),        # X-AXIS: array indices
                y=arr,                          # Y-AXIS: array values
                marker_color=colors,            # Bar colors
                customdata=hover_labels,        # Custom hover text
                hovertemplate="%{y}<br>%{customdata}<extra></extra>",
                text=arr,                       # Show value on each bar
                textposition="inside",          # Place text inside bars
                textfont=dict(                  # Manage text font styling
                    color="white",
                    size=14,
                    family="Arial",
                ),
            )
        ]
    )

    # Configure chart layout
    fig.update_layout(
        showlegend=False,
        yaxis_title="Value",
        height=400,
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            title=f"Finished Sorted Array: {arr}" if finished else "",
        ),
    )

    return fig

# --------------------------------------------------------------------------------------------------
# UI CONTROL FUNCTIONS
# --------------------------------------------------------------------------------------------------

def next_step(stepper):
    """
    This function is called when the user clicks "Next Step" and advances
    the sorting algorithm by one step, updating the visualization.
    
    Args:
        stepper (generator or None): The merge sort step generator
        
    Returns:
        tuple: Updated state values for all UI components:
            - generator: Updated stepper state
            - str: progress_txtbox message
            - Figure: Updated plot
            - gr.update: Next step button state
            - gr.update: Reset button state
    """

    # Handle case where stepper is not initialized
    if stepper is None:
        return (
            stepper,
            "❌ No sorting in progress!",
            None,
            gr.update(),
            gr.update()
        )

    try:
        # Get the next step from the generator
        step_type, message, current_array, highlight_range = next(stepper)

        # Create visualization for this step
        plot = create_bar_plot(current_array, highlight_range)
        
        return (
            stepper,                  # Keep stepper for next iteration
            message,                  # Display step message
            plot,                     # Update plot
            gr.update(),              # Keep next step button visible
            gr.update()               # Keep reset button hidden
        )

    except StopIteration as e:
        # Sorting is finished - get final array
        final_array = e.value if e.value is not None else unsorted_array
        final_plot = create_bar_plot(final_array, finished=True)
        
        return (
            None,                        # Clear stepper
            f"🏆 Sorting complete! \n✅ Final Result: {final_array}",
            final_plot,                  # Show final plot
            gr.update(visible=False),    # Hide next step button    
            gr.update(visible=True)      # Show reset button
        )


def start_sorting():
    """
    This function is called when user clicks "Start Sorting" and sets up
    the initial state for the step-by-step visualization.
    
    Returns:
        tuple: Initial state values for all UI components
    """
    # NOTE: No need to validate that an array has been generated before start sorting button is presssed
    # because it is disabled until an array is generated anyway

    # Create the merge sort stepper generator
    stepper = visualize_merge_sort_steps(unsorted_array)

    # Create initial visualization of unsorted array
    initial_plot = create_bar_plot(unsorted_array)

    return (
        stepper,                                      # Store stepper in state
        gr.update(                                    # Update progress textbox
            value=(
                "Here is a graphical representation of the unsorted array.\n"
                "Click 'Next Step' to begin sorting the bars!"
            ),
            visible=True,
        ),
        gr.update(visible=False),                     # Hide length input textbox
        gr.update(visible=False),                     # Hide generate button
        gr.update(visible=False),                     # Hide array display textbox
        gr.update(visible=False),                     # Hide start sorting button
        gr.update(value=initial_plot, visible=True),  # Show barplot area
        gr.update(visible=True),                      # Show next step button
    )


def reset_app():
    """
    Clears all data and returns the UI to the starting configuration
    so the user can generate and sort a new array.
    
    Returns:
        tuple: Reset state values for all UI components
    """

    #Clear the global array
    unsorted_array.clear()

    return (
        None,                                                  # Clear stepper state
        gr.update(value="", visible=False),                    # Hide progress textbox
        gr.update(value=None, visible=False),                  # Hide barplot area
        gr.update(value="", visible=True, interactive=True),   # Show length input textbox
        gr.update(visible=True, interactive=True),             # Show generate button
        gr.update(value="", visible=True),                     # Show array display textbox
        gr.update(visible=True, interactive=False),            # Show disabled start button
        gr.update(visible=False),                              # Hide next step button
        gr.update(visible=False),                              # Hide reset button
    )

# --------------------------------------------------------------------------------------------------
# GRADIO USER INTERFACE
# --------------------------------------------------------------------------------------------------

with gr.Blocks(theme=gr.themes.Citrus()) as demo:
    # State variable to maintain stepper across function calls
    stepper_state = gr.State(None)

    #Title of program
    gr.Markdown(
        "<h1 style='text-align:center; font-size: 36px;'>🎮 Learn Merge Sort – The Game!</h1>"
    )

    # Input section
    length_input_txtbox = gr.Textbox(
        label="Array Length",
        placeholder=f"Enter a number between 1 and {MAX_ARRAY_LENGTH}",
        info="Choose how many numbers you want in your array"
    )

    # Progress/Status display
    progress_txtbox = gr.Textbox(
        label="What's going on now?",
        interactive=False,
        visible=False,
        lines=3,
    )

    # Generate array page
    generate_btn = gr.Button(" Generate Random Array 🎲")
    array_display_txtbox = gr.Textbox(label="Generated Unsorted Array")
    start_sorting_btn = gr.Button("Start Sorting ▶️", interactive=False)

    # Visualize sorting page
    barplot_area = gr.Plot(label="Sorting Progress", visible=False)
    next_step_btn = gr.Button("Next Step ➡️", visible=False)
    reset_btn = gr.Button("Try Another? 🔄", visible=False)

# --------------------------------------------------------------------------------------------------
# EVENT HANDLERS - Connect UI elements to functions
# --------------------------------------------------------------------------------------------------

    # Generate array when button clicked
    generate_btn.click(
        fn=generate_random_array,
        inputs=length_input_txtbox,
        outputs=[
            array_display_txtbox,
            generate_btn,
            length_input_txtbox,
            start_sorting_btn
        ]
    )

    # Start sorting process when button clicked
    start_sorting_btn.click(
        fn=start_sorting,
        inputs=[],
        outputs=[
            stepper_state,
            progress_txtbox,
            length_input_txtbox,
            generate_btn,
            array_display_txtbox,
            start_sorting_btn,
            barplot_area,
            next_step_btn
        ]
    )

    # Advance to next sorting step when button clicked
    next_step_btn.click(
        fn=next_step,
        inputs=[stepper_state],
        outputs=[
            stepper_state,
            progress_txtbox,
            barplot_area,
            next_step_btn,
            reset_btn
        ]
    )

    # Reset application when button clicked
    reset_btn.click(
        fn=reset_app,
        inputs=None,
        outputs=[
            stepper_state,
            progress_txtbox,
            barplot_area,
            length_input_txtbox,
            generate_btn,
            array_display_txtbox,
            start_sorting_btn,
            next_step_btn,
            reset_btn
        ]
    )

# --------------------------------------------------------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    demo.launch()
