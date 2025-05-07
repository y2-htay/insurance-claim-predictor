def prepare_model_evaluation(data):
    try:
        results = []
        for name, (sv, ae) in enumerate(zip(data['settlement_values'], data['absolute_errors']), start=1):
            accuracy = 100 - (ae / sv * 100) if sv != 0 else 0
            results.append({
                'settlement_value': round(sv),
                'accuracy': round(accuracy, 2)
            })
    except:
        return None

    return results
