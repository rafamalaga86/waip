
def getMetacriticScoreColour(score):
    try:
        score = int(score)
        if score >= 75:
            return '#6c3'
        elif score >= 50:
            return '#fc3'
        else:
            return '#f00'
    except ValueError:
        return '#6c3'
