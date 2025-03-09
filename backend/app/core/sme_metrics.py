from typing import Dict
import pandas as pd

class FinancialMetrics:
    """Calculates a more robust confidence score using multiple financial indicators."""

    @staticmethod
    def calculate_metrics(data: Dict):
        """Computes confidence score and other key financial indicators."""

        def safe_extract(df, column, default=0):
            """Safely extracts a value from a DataFrame column."""
            if not df.empty and column in df.columns and not df[column].isna().all():
                value = df[column].iloc[0]
                try:
                    return float(value) if pd.api.types.is_numeric_dtype(df[column]) else default
                except ValueError:
                    return default
            return default

        # Load data into DataFrames
        df_sales = pd.DataFrame(data.get("supercia", []))
        df_credit = pd.DataFrame(data.get("scoreburo", []))
        df_salary = pd.DataFrame(data.get("salario", []))
        df_vehicles = pd.DataFrame(data.get("auto", []))
        df_establishments = pd.DataFrame(data.get("extablecimiento", []))

        # Extract values safely
        ventas = safe_extract(df_sales, "ventas")
        impuesto_renta = safe_extract(df_sales, "impuestoRenta")
        cupo_creditos = safe_extract(df_credit, "cupoCreditos")
        salario = safe_extract(df_salary, "valorSalario")
        score = safe_extract(df_credit, "score")
        prob_morosidad = safe_extract(df_credit, "probMorosidad")
        num_establishments = safe_extract(df_establishments, "numeroEstablecimientos")

        # Asset Valuation (Summing vehicle values)
        auto_valuation = df_vehicles["precioVenta"].sum() if not df_vehicles.empty else 0.0

        # Compute Financial Ratios
        total_income = ventas + salario + auto_valuation
        financing_percentage = (cupo_creditos / total_income * 100) if total_income > 0 else 0
        tax_burden = (impuesto_renta / ventas * 100) if ventas > 0 else 0
        debt_to_income = (cupo_creditos / total_income * 100) if total_income > 0 else 0

        # Determine Credit Need
        needs_credit = "YES" if financing_percentage < 30 or financing_percentage > 40 else "NO"

        # Calculate Confidence Score (Weighted Model)
        confidence_score = (
            (score * 0.4) +  # Credit Score (40%)
            (min(salario / 5000, 1) * 200 * 0.2) +  # Salary Contribution (20%)
            (min(ventas / 1000000, 1) * 300 * 0.2) +  # Sales Contribution (20%)
            ((1 - prob_morosidad / 100) * 200 * 0.1) +  # Risk Adjustment (10%)
            (min(num_establishments / 5, 1) * 100 * 0.1)  # Business Stability (10%)
        )

        # Normalize Confidence Score (0-1000)
        confidence_score = max(0, min(1000, confidence_score))

        return {
            "Confidence Score": int(confidence_score),
            "Financing %": round(financing_percentage, 2),
            "Tax Burden %": round(tax_burden, 2),
            "Debt-to-Income %": round(debt_to_income, 2),
            "Needs Credit": needs_credit,
            "Assets Valuation": round(total_income, 2),
        }