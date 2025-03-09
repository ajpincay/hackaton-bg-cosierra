from typing import Dict
import pandas as pd

class FinancialMetrics:
    """Calculates financial metrics for SMEs."""

    @staticmethod
    def calculate_metrics(data: Dict):
        """Computes key financial indicators from structured data."""

        def safe_extract(df, column, default=0):
            """Safely extracts a value from a DataFrame column and converts to Python types."""
            if not df.empty and column in df.columns:
                value = df[column].iloc[0]
                return int(value) if isinstance(value, (int, float, pd.Int64Dtype, pd.Float64Dtype)) else default
            return default

        df_sales = pd.DataFrame(data.get("supercia", []))
        df_credit = pd.DataFrame(data.get("scoreburo", []))
        df_salary = pd.DataFrame(data.get("salario", []))
        df_vehicles = pd.DataFrame(data.get("auto", []))

        # Extract values safely and convert them to Python-native types
        ventas = safe_extract(df_sales, "ventas")
        impuesto_renta = safe_extract(df_sales, "impuestoRenta")
        cupo_creditos = safe_extract(df_credit, "cupoCreditos")
        salario = safe_extract(df_salary, "valorSalario")
        auto_valuation = df_vehicles["precioVenta"].sum() if not df_vehicles.empty else 0

        # Ensure auto_valuation is a standard float type
        auto_valuation = float(auto_valuation)

        # Compute Ratios
        total_income = ventas + salario + auto_valuation
        financing_percentage = (cupo_creditos / total_income) * 100 if total_income > 0 else 0
        tax_burden = (impuesto_renta / ventas) * 100 if ventas > 0 else 0
        dti_ratio = (cupo_creditos / total_income) * 100 if total_income > 0 else 0

        # Predict if Credit is Needed
        needs_credit = "YES" if financing_percentage < 30 or dti_ratio > 40 else "NO"

        return {
            "Confidence Score": int(safe_extract(df_credit, "score")),
            "Financing %": round(float(financing_percentage), 2),
            "Tax Burden %": round(float(tax_burden), 2),
            "Debt-to-Income %": round(float(dti_ratio), 2),
            "Needs Credit": needs_credit,
            "Assets Valuation": round(float(auto_valuation + ventas + salario), 2),
        }