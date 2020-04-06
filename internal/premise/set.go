package premise

import (
	"fmt"

	"github.com/merenbach/syllogism/internal/article"
	"github.com/merenbach/syllogism/internal/help"
	"github.com/merenbach/syllogism/internal/symbol"
	"github.com/merenbach/syllogism/internal/term"
)

// Set of all premises.
type Set []*Premise

// // Find the index of a premise with a given line number.
// // Find will return (-1) if no matching premises are found.
// func (ps Set) Find(n int) int {
// 	for i, p := range ps {
// 		if p.Number == n {
// 			return i
// 		}
// 	}
// 	return (-1)
// }

// Compute a conclusion.
func (ps Set) Compute(negativePremiseCount int, symbol1 *symbol.Symbol, symbol2 *symbol.Symbol) string {
	if len(ps) == 0 {
		return "A is A"
	}

	// if ps.NegativePremiseCount() == 0 {
	if negativePremiseCount == 0 {
		// affirmative conclusion
		// TODO: can we push more of these conditionals inside the symbol type?
		if symbol1.DistributionCount > 0 {
			return symbol1.ConclusionForAllIs(symbol2)
		} else if symbol2.DistributionCount > 0 {
			return symbol2.ConclusionForAllIs(symbol1)
		} else if symbol1.ArticleType != article.TypeNone || symbol2.ArticleType == article.TypeNone {
			return symbol1.ConclusionForSomeIs(symbol2)
		} else {
			return symbol2.ConclusionForSomeIs(symbol1)
		}

	} else {
		// negative conclusion
		if symbol2.DistributionCount == 0 {
			return fmt.Sprintf("Some %s is not %s%s", symbol2.Term, symbol1.ArticleType, symbol1.Term)
		} else if symbol1.DistributionCount == 0 {
			return fmt.Sprintf("Some %s is not %s%s", symbol1.Term, symbol2.ArticleType, symbol2.Term)
		} else if symbol1.TermType == term.TypeDesignator {
			return fmt.Sprintf("%s is not %s%s", symbol1.Term, symbol2.ArticleType, symbol2.Term)
		} else if symbol2.TermType == term.TypeDesignator {
			return fmt.Sprintf("%s is not %s%s", symbol2.Term, symbol1.ArticleType, symbol1.Term)
		} else if symbol1.ArticleType == article.TypeNone && symbol2.ArticleType != article.TypeNone {
			return fmt.Sprintf("No %s is %s%s", symbol2.Term, symbol1.ArticleType, symbol1.Term)
		} else {
			return fmt.Sprintf("No %s is %s%s", symbol1.Term, symbol2.ArticleType, symbol2.Term)
		}
	}
}

// List output for premises, optionally in distribution-analysis format.
// This may be used for link-order output if the premise set is arranged accordingly.
// TODO: use tabwriter for distribution-analysis format?
func (ps Set) List(analyze bool) error {
	if len(ps) == 0 {
		return fmt.Errorf(help.NoPremises)
	}

	for _, prem := range ps {
		if !analyze {
			fmt.Printf("%d  %s\n", prem.Number, prem.Statement)
		} else {
			fmt.Printf("%d  ", prem.Number)

			if prem.Form < 6 && prem.Predicate.TermType == term.TypeDesignator {
				prem.Form += 2
			}

			if prem.Form < 4 {
				fmt.Printf("%s  ", prem.Form.Quantifier())
			}

			fmt.Printf("%s%s%s  %s%s\n", prem.Subject.Term, prem.Form.Subject(), prem.Form.Copula(), prem.Predicate.Term, prem.Form.Predicate())
		}
	}
	return nil
}

// // NegativePremiseCount returns the count of negative premises.
// TODO: this should probably actually return the slice of negative premises, and then we can do len() on that
// func (ps Set) NegativePremiseCount() int {
// 	var negativePremises int
// 	for _, p := range ps {
// 		if p.Form.IsNegative() {
// 			negativePremises++
// 		}
// 	}
// 	return negativePremises
// }