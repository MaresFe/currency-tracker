"""
Currency Exchange Rate Tracker
Real-time currency exchange rates with GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
import pandas as pd
import json
from pathlib import Path


class CurrencyTracker:
    def __init__(self):
        # Free API - no key required
        self.api_url = "https://api.frankfurter.app/latest"
        self.base_currency = "USD"
        self.history = []
        
    def get_exchange_rates(self, base="USD"):
        """Get current exchange rates for a base currency"""
        try:
            params = {"from": base}
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            rates = {
                'base': data['base'],
                'date': data['date'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'rates': data['rates']
            }
            
            return rates, None
            
        except requests.exceptions.RequestException as e:
            return None, f"Network error: {str(e)}"
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def get_conversion(self, amount, from_currency, to_currency):
        """Convert amount from one currency to another"""
        try:
            url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            converted_amount = data['rates'][to_currency]
            
            return converted_amount, None
            
        except Exception as e:
            return None, f"Conversion error: {str(e)}"
    
    def save_to_history(self, rates_data):
        """Save current rates to history"""
        self.history.append(rates_data)


class CurrencyTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Exchange Rate Tracker")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.tracker = CurrencyTracker()
        self.current_rates = None
        self.auto_refresh = False
        self.refresh_job = None
        
        # Popular currencies to display
        self.display_currencies = ['EUR', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD', 
                                   'CNY', 'TRY', 'INR', 'BRL', 'MXN', 'ZAR']
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#16a34a', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="💱 Currency Exchange Rate Tracker",
            font=('Arial', 20, 'bold'),
            bg='#16a34a',
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f9ff')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Control panel
        control_frame = tk.Frame(main_frame, bg='#f0f9ff')
        control_frame.pack(fill='x', pady=(0, 15))
        
        # Base currency selector
        tk.Label(
            control_frame,
            text="Base Currency:",
            font=('Arial', 10, 'bold'),
            bg='#f0f9ff'
        ).pack(side='left', padx=(0, 10))
        
        self.base_currency_var = tk.StringVar(value='USD')
        base_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CHF', 'TRY']
        
        base_combo = ttk.Combobox(
            control_frame,
            textvariable=self.base_currency_var,
            values=base_currencies,
            state='readonly',
            width=10,
            font=('Arial', 10)
        )
        base_combo.pack(side='left', padx=(0, 20))
        
        # Refresh button
        self.refresh_btn = tk.Button(
            control_frame,
            text="🔄 Refresh Rates",
            command=self.refresh_rates,
            font=('Arial', 10, 'bold'),
            bg='#2563eb',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.refresh_btn.pack(side='left', padx=5)
        
        # Auto-refresh toggle
        self.auto_refresh_var = tk.BooleanVar(value=False)
        auto_refresh_cb = tk.Checkbutton(
            control_frame,
            text="Auto-refresh (60s)",
            variable=self.auto_refresh_var,
            command=self.toggle_auto_refresh,
            font=('Arial', 9),
            bg='#f0f9ff',
            cursor='hand2'
        )
        auto_refresh_cb.pack(side='left', padx=10)
        
        # Export button
        self.export_btn = tk.Button(
            control_frame,
            text="💾 Export to Excel",
            command=self.export_to_excel,
            font=('Arial', 10, 'bold'),
            bg='#16a34a',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            state='disabled'
        )
        self.export_btn.pack(side='left', padx=5)
        
        # Status bar
        status_frame = tk.Frame(main_frame, bg='#e0f2fe', relief='solid', borderwidth=1)
        status_frame.pack(fill='x', pady=(0, 15))
        
        self.status_label = tk.Label(
            status_frame,
            text="Click 'Refresh Rates' to get current exchange rates",
            font=('Arial', 9),
            bg='#e0f2fe',
            fg='#0c4a6e',
            padx=10,
            pady=8
        )
        self.status_label.pack()
        
        # Last update time
        self.update_time_label = tk.Label(
            main_frame,
            text="",
            font=('Arial', 8, 'italic'),
            bg='#f0f9ff',
            fg='#64748b'
        )
        self.update_time_label.pack()
        
        # Rates display frame
        rates_frame = tk.LabelFrame(
            main_frame,
            text="Exchange Rates",
            font=('Arial', 11, 'bold'),
            bg='#f0f9ff',
            fg='#0f172a'
        )
        rates_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        # Create Treeview for rates
        columns = ('Currency', 'Rate', 'Change')
        self.rates_tree = ttk.Treeview(
            rates_frame,
            columns=columns,
            show='headings',
            height=12
        )
        
        # Define headings
        self.rates_tree.heading('Currency', text='Currency')
        self.rates_tree.heading('Rate', text='Exchange Rate')
        self.rates_tree.heading('Change', text='24h Change')
        
        # Define column widths
        self.rates_tree.column('Currency', width=200, anchor='center')
        self.rates_tree.column('Rate', width=250, anchor='center')
        self.rates_tree.column('Change', width=200, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(rates_frame, orient='vertical', command=self.rates_tree.yview)
        self.rates_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.rates_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview", rowheight=35, font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        
        # Converter section
        converter_frame = tk.LabelFrame(
            main_frame,
            text="Currency Converter",
            font=('Arial', 11, 'bold'),
            bg='#f0f9ff',
            fg='#0f172a'
        )
        converter_frame.pack(fill='x', pady=(15, 0))
        
        converter_inner = tk.Frame(converter_frame, bg='#f0f9ff')
        converter_inner.pack(padx=20, pady=15)
        
        # Amount entry
        tk.Label(
            converter_inner,
            text="Amount:",
            font=('Arial', 10),
            bg='#f0f9ff'
        ).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        
        self.amount_entry = tk.Entry(
            converter_inner,
            font=('Arial', 10),
            width=15
        )
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)
        self.amount_entry.insert(0, "100")
        
        # From currency
        tk.Label(
            converter_inner,
            text="From:",
            font=('Arial', 10),
            bg='#f0f9ff'
        ).grid(row=0, column=2, padx=5, pady=5, sticky='e')
        
        self.from_currency_var = tk.StringVar(value='USD')
        from_combo = ttk.Combobox(
            converter_inner,
            textvariable=self.from_currency_var,
            values=base_currencies,
            state='readonly',
            width=10,
            font=('Arial', 10)
        )
        from_combo.grid(row=0, column=3, padx=5, pady=5)
        
        # To currency
        tk.Label(
            converter_inner,
            text="To:",
            font=('Arial', 10),
            bg='#f0f9ff'
        ).grid(row=0, column=4, padx=5, pady=5, sticky='e')
        
        self.to_currency_var = tk.StringVar(value='EUR')
        to_combo = ttk.Combobox(
            converter_inner,
            textvariable=self.to_currency_var,
            values=self.display_currencies + base_currencies,
            state='readonly',
            width=10,
            font=('Arial', 10)
        )
        to_combo.grid(row=0, column=5, padx=5, pady=5)
        
        # Convert button
        convert_btn = tk.Button(
            converter_inner,
            text="Convert",
            command=self.convert_currency,
            font=('Arial', 10, 'bold'),
            bg='#f59e0b',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2'
        )
        convert_btn.grid(row=0, column=6, padx=10, pady=5)
        
        # Result label
        self.convert_result_label = tk.Label(
            converter_frame,
            text="",
            font=('Arial', 12, 'bold'),
            bg='#f0f9ff',
            fg='#16a34a'
        )
        self.convert_result_label.pack(pady=(0, 15))
        
    def refresh_rates(self):
        """Refresh exchange rates"""
        self.refresh_btn.config(state='disabled')
        self.status_label.config(text="Fetching exchange rates...", fg='#0c4a6e')
        self.root.update_idletasks()
        
        base = self.base_currency_var.get()
        rates_data, error = self.tracker.get_exchange_rates(base)
        
        if error:
            self.status_label.config(text=f"Error: {error}", fg='#dc2626')
            messagebox.showerror("Error", error)
            self.refresh_btn.config(state='normal')
            return
        
        self.current_rates = rates_data
        self.tracker.save_to_history(rates_data)
        
        # Update display
        self.update_rates_display(rates_data)
        
        # Update status
        self.status_label.config(
            text=f"✓ Rates updated successfully | Base: {rates_data['base']} | Date: {rates_data['date']}",
            fg='#16a34a'
        )
        self.update_time_label.config(text=f"Last updated: {rates_data['timestamp']}")
        
        self.export_btn.config(state='normal')
        self.refresh_btn.config(state='normal')
        
    def update_rates_display(self, rates_data):
        """Update the treeview with current rates"""
        # Clear existing items
        for item in self.rates_tree.get_children():
            self.rates_tree.delete(item)
        
        # Add new rates
        rates = rates_data['rates']
        
        # Currency full names
        currency_names = {
            'EUR': 'Euro (EUR)',
            'GBP': 'British Pound (GBP)',
            'JPY': 'Japanese Yen (JPY)',
            'CHF': 'Swiss Franc (CHF)',
            'CAD': 'Canadian Dollar (CAD)',
            'AUD': 'Australian Dollar (AUD)',
            'CNY': 'Chinese Yuan (CNY)',
            'TRY': 'Turkish Lira (TRY)',
            'INR': 'Indian Rupee (INR)',
            'BRL': 'Brazilian Real (BRL)',
            'MXN': 'Mexican Peso (MXN)',
            'ZAR': 'South African Rand (ZAR)'
        }
        
        for currency in self.display_currencies:
            if currency in rates:
                rate = rates[currency]
                name = currency_names.get(currency, currency)
                
                # Format rate
                if rate > 100:
                    rate_str = f"{rate:,.2f}"
                else:
                    rate_str = f"{rate:.4f}"
                
                # Calculate change (simplified - would need historical data for real change)
                change = "N/A"
                
                self.rates_tree.insert('', 'end', values=(name, rate_str, change))
    
    def convert_currency(self):
        """Convert currency based on user input"""
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_currency_var.get()
            to_curr = self.to_currency_var.get()
            
            if from_curr == to_curr:
                messagebox.showwarning("Warning", "Please select different currencies")
                return
            
            result, error = self.tracker.get_conversion(amount, from_curr, to_curr)
            
            if error:
                messagebox.showerror("Error", error)
                return
            
            self.convert_result_label.config(
                text=f"{amount:,.2f} {from_curr} = {result:,.2f} {to_curr}"
            )
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh functionality"""
        if self.auto_refresh_var.get():
            self.auto_refresh = True
            self.schedule_refresh()
        else:
            self.auto_refresh = False
            if self.refresh_job:
                self.root.after_cancel(self.refresh_job)
                self.refresh_job = None
    
    def schedule_refresh(self):
        """Schedule next refresh"""
        if self.auto_refresh:
            self.refresh_rates()
            # Schedule next refresh in 60 seconds
            self.refresh_job = self.root.after(60000, self.schedule_refresh)
    
    def export_to_excel(self):
        """Export current rates and history to Excel"""
        if not self.current_rates:
            messagebox.showwarning("No Data", "No rates to export!")
            return
        
        try:
            # Prepare current rates data
            rates_list = []
            base = self.current_rates['base']
            
            for currency, rate in self.current_rates['rates'].items():
                rates_list.append({
                    'Base Currency': base,
                    'Target Currency': currency,
                    'Exchange Rate': rate,
                    'Date': self.current_rates['date'],
                    'Timestamp': self.current_rates['timestamp']
                })
            
            df_current = pd.DataFrame(rates_list)
            
            # Generate filename
            filename = f"exchange_rates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            # Create Excel writer
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df_current.to_excel(writer, sheet_name='Current Rates', index=False)
                
                # If history exists, add it
                if self.tracker.history:
                    history_list = []
                    for record in self.tracker.history:
                        for currency, rate in record['rates'].items():
                            history_list.append({
                                'Base': record['base'],
                                'Currency': currency,
                                'Rate': rate,
                                'Date': record['date'],
                                'Timestamp': record['timestamp']
                            })
                    
                    df_history = pd.DataFrame(history_list)
                    df_history.to_excel(writer, sheet_name='History', index=False)
            
            messagebox.showinfo(
                "Success",
                f"Exported exchange rates to:\n{filename}"
            )
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export:\n{str(e)}")


def main():
    root = tk.Tk()
    app = CurrencyTrackerGUI(root)
    
    # Ask to fetch rates on startup
    if messagebox.askyesno("Fetch Rates", "Would you like to fetch current exchange rates now?"):
        root.after(100, app.refresh_rates)
    
    root.mainloop()


if __name__ == "__main__":
    main()
