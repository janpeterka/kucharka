class TipApprover:
    def approve(tip):
        tip.is_approved = True
        tip.is_hidden = False
        tip.save()

    def disapprove(tip):
        tip.is_approved = False
        tip.is_hidden = True
        tip.save()
