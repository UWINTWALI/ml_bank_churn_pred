# Business KPIs calculator
def calculate_kpis(df, predictions):
    """Calculate business KPIs from predictions"""
    total = len(df)
    churners = predictions.sum()
    rate = churners / total
    
    # Business logic: $1000/customer saved, $200/false positive
    net_value = churners * 1000 - (total - churners) * 200
    
    return {
        'total': total,
        'churners': churners,
        'rate': rate,
        'net_value': net_value
    }
