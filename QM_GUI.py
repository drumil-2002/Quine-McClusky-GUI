import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time

class QuineMcCluskeyMinimizer:

    def __init__(self, mt_input, dc_input):
        self.mt_input = mt_input
        self.dc_input = dc_input
        self.size = 0
        self.groups = {}
        self.all_pi = set()
        self.chart = {}
        self.minterms = []
        self.dc_list = []

    # to parse and sort minterms and don't-care
    def parse_inputs(self):
        self.minterms = [int(i) for i in self.mt_input.split(",") if i]
        self.dc_list = [int(i) for i in self.dc_input.split(",") if self.dc_input]
        self.minterms.sort()
        combined_terms = self.minterms + self.dc_list
        combined_terms.sort()
        self.size = len(bin(combined_terms[-1])) - 2
        self._group_terms(combined_terms)
        
    # to group terms by the number of 1s in their binary representation
    def _group_terms(self, terms):
        for term in terms:
            count_ones = bin(term).count('1')
            binary_term = bin(term)[2:].zfill(self.size)
            self.groups.setdefault(count_ones, []).append(binary_term)
            
    # to compare two binary terms to find if they differ by one bit
    @staticmethod
    def compare_terms(a, b):
        mismatch_count = 0
        mismatch_index = None
        for idx, (bit_a, bit_b) in enumerate(zip(a, b)):
            if bit_a != bit_b:
                mismatch_count += 1
                mismatch_index = idx
                if mismatch_count > 1:
                    return False, None
        return mismatch_count == 1, mismatch_index

    # Expand a binary term into all possible minterms
    @staticmethod
    def find_minterms(term):
        gaps = term.count('-')
        if gaps == 0:
            return [str(int(term, 2))]
        replacements = [bin(i)[2:].zfill(gaps) for i in range(2**gaps)]
        results = []
        for replacement in replacements:
            temp = term
            for bit in replacement:
                temp = temp.replace('-', bit, 1)
            results.append(str(int(temp, 2)))
        return results
    
    # to execute algorithm
    def execute_algorithm(self):
        self.parse_inputs()
        while True:
            new_groups = {}
            marked = set()
            stop = True

            for group_key, terms in sorted(self.groups.items()):
                if group_key + 1 not in self.groups:
                    continue
                for term1 in terms:
                    for term2 in self.groups[group_key + 1]:
                        similar, index = self.compare_terms(term1, term2)
                        if similar:
                            stop = False
                            new_term = term1[:index] + '-' + term1[index + 1:]
                            new_groups.setdefault(group_key, []).append(new_term)
                            marked.update({term1, term2})
            self.all_pi.update(set().union(*self.groups.values()) - marked)
            if stop:
                break
            self.groups = new_groups

        self._build_chart()

    # build the chart of PI
    def _build_chart(self):
        for pi in self.all_pi:
            for minterm in self.find_minterms(pi):
                if int(minterm) not in self.dc_list:
                    self.chart.setdefault(minterm, []).append(pi)

    # identify EPI
    def find_essential_pis(self):
        essential_pis = []
        for minterm, pis in self.chart.items():
            if len(pis) == 1:
                essential_pi = pis[0]
                if essential_pi not in essential_pis:
                    essential_pis.append(essential_pi)
        return essential_pis

    # generate the minimized equation
    def generate_solution(self):
        essential_pis = self.find_essential_pis()
        self._remove_covered_terms(essential_pis)
        if not self.chart:
            final_result = [self._find_variables(pi) for pi in essential_pis]
        else:
            prime_cover = [self._find_variables(pi) for pis in self.chart.values() for pi in pis]
            minimal_cover = min(prime_cover, key=len)
            final_result = [minimal_cover] + [self._find_variables(pi) for pi in essential_pis]
            
        sop_expression = " + ".join("".join(term) for term in final_result)
        self.product_term_count = len(sop_expression.split(" + "))
        
        return sop_expression
    # convert binary term into variables
    @staticmethod
    def _find_variables(binary_term):
        variables = []
        for idx, bit in enumerate(binary_term):
            if bit == '1':
                variables.append(chr(idx + 65))
            elif bit == '0':
                variables.append(chr(idx + 65) + "'")
        return variables

    # to remove minterms covered by EPI
    def _remove_covered_terms(self, essential_pis):
        for pi in essential_pis:
            for minterm in self.find_minterms(pi):
                self.chart.pop(minterm, None)

    # SOP to POS
    def sop_to_pos(self, sop_expression):
        terms = sop_expression.split(" + ")
        pos_terms = []
        for term in terms:
            literals = []
            for char in term:
                if char.isalpha():
                    if term.index(char) + 1 < len(term) and term[term.index(char) + 1] == "'":
                        literals.append(char)
                    else:
                        literals.append(char + "'")
            pos_terms.append(f"({' + '.join(literals)})")
        return " . ".join(pos_terms)

class QuineMcCluskeyGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quine-McCluskey Minimizer")
        self.root.geometry("900x650")
        self.root.configure(bg="#e3f2fd")
        self._build_interface()

    def _build_interface(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', font=('Helvetica', 14), background="#e3f2fd", foreground="#1a237e")
        style.configure('TButton', font=('Helvetica', 12, 'bold'), background='#1e88e5', foreground='white',
                        borderwidth=2, padding=10)
        style.map('TButton', background=[('active', '#0d47a1')])
        style.configure('TEntry', font=('Helvetica', 14))

        title_label = tk.Label(
            self.root,
            text="Quine-McCluskey Minimizer",
            font=("Helvetica", 24, "bold"),
            bg="#0288d1",
            fg="white",
            pady=10,
        )
        title_label.pack(fill=tk.X, pady=(10, 20))

        # Input
        input_frame = tk.Frame(self.root, bg="#e3f2fd")
        input_frame.pack(pady=10, padx=20, fill=tk.X)

        tk.Label(input_frame, text="Enter Minterms (comma-separated):", bg="#e3f2fd", font=("Helvetica", 14)).grid(
            row=0, column=0, sticky="e", padx=10, pady=5
        )
        self.minterms_entry = ttk.Entry(input_frame, width=100)
        self.minterms_entry.grid(row=0, column=1, pady=5)

        tk.Label(input_frame, text="Enter Don't Cares (comma-separated):", bg="#e3f2fd", font=("Helvetica", 14)).grid(
            row=1, column=0, sticky="e", padx=10, pady=5
        )
        self.dontcares_entry = ttk.Entry(input_frame, width=100)
        self.dontcares_entry.grid(row=1, column=1, pady=5)

        # Buttons
        button_frame = tk.Frame(self.root, bg="#e3f2fd")
        button_frame.pack(pady=20)

        calculate_button = ttk.Button(button_frame, text="Calculate", command=self.calculate)
        calculate_button.grid(row=0, column=0, padx=15)

        convert_button = ttk.Button(button_frame, text="Convert to POS", command=self.convert_to_pos)
        convert_button.grid(row=0, column=1, padx=15)

        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_inputs)
        clear_button.grid(row=0, column=2, padx=15)

        load_file_button = ttk.Button(button_frame, text="Load File", command=self.load_file)
        load_file_button.grid(row=0, column=3, padx=15)

        save_output_button = ttk.Button(button_frame, text="Save Output", command=self.save_output)
        save_output_button.grid(row=0, column=4, padx=15)

        # Output
        output_frame = tk.Frame(self.root, bg="#e3f2fd")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        output_label = tk.Label(output_frame, text="Output:", bg="#e3f2fd", font=("Helvetica", 14, "bold"))
        output_label.pack(anchor="nw", pady=5)

        self.output_box = tk.Text(
            output_frame, height=15, wrap=tk.WORD, font=("Helvetica", 14), bg="#f1f8e9", fg="#1b5e20"
        )
        self.output_box.pack(fill=tk.BOTH, expand=True, pady=5)

    def calculate(self):
        minterms = self.minterms_entry.get()
        dontcares = self.dontcares_entry.get()

        try:
            start_time = time.perf_counter()
            qmc = QuineMcCluskeyMinimizer(minterms, dontcares)
            qmc.execute_algorithm()
            solution = qmc.generate_solution()
            elapsed_time = round(time.perf_counter() - start_time, 10)

            self.output_box.delete(1.0, tk.END)
            self.output_box.insert(tk.END, f"Minimized Expression (SOP):\n{solution}\n")
            self.output_box.insert(tk.END, f"Number of Product Terms: {qmc.product_term_count}\n")
            self.output_box.insert(tk.END, f"Execution Time: {elapsed_time:.6f} seconds\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def convert_to_pos(self):
        try:
            current_text = self.output_box.get("1.0", tk.END).strip()
            if not current_text.startswith("Minimized Expression (SOP):"):
                raise ValueError("Minimized SOP expression not found in output.")

            sop_expression = current_text.split("\n")[1]
            qmc = QuineMcCluskeyMinimizer("", "")
            pos_expression = qmc.sop_to_pos(sop_expression)

            self.output_box.insert(tk.END, f"\nPOS:\n{pos_expression}\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_inputs(self):
        self.minterms_entry.delete(0, tk.END)
        self.dontcares_entry.delete(0, tk.END)
        self.output_box.delete(1.0, tk.END)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                if len(lines) < 2:
                    raise ValueError("The file must contain at least two lines (minterms and don't cares).")
                self.minterms_entry.delete(0, tk.END)
                self.minterms_entry.insert(0, lines[0].strip())
                self.dontcares_entry.delete(0, tk.END)
                self.dontcares_entry.insert(0, lines[1].strip())
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file: {e}")

    def save_output(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.output_box.get(1.0, tk.END).strip())
                messagebox.showinfo("Success", "Output saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = QuineMcCluskeyGUI()
    app.run()