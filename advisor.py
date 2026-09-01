def financial_advice(kpi):

    advice=[]

    if kpi["expense"]>kpi["income"]:

        advice.append(
            "Expenses exceed income."
        )

    if kpi["balance"]<10000:

        advice.append(
            "Maintain higher emergency fund."
        )

    if len(advice)==0:

        advice.append(
            "Financial health looks good."
        )

    return advice