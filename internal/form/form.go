package form

// A Form of syllogism.
type Form int

// TODO: use iota
// TODO: should be able to swap ordering of any of these and retain same functionality once refactor is complete
//       since we won't be relying on integer values anymore
const (
	Undefined      Form = (-1)
	SomeAIsB            = 0 // Type I (particular affirmative)
	SomeAIsNotB         = 1 // Type O (particular negative)
	AllAIsB             = 2 // Type A (universal affirmative)
	NoAIsB              = 3 // Type E (universal negative)
	AIsT                = 4
	AIsNotT             = 5
	AEqualsT            = 6
	ADoesNotEqualT      = 7
)

const (
	// WordAll is the word "all."
	WordAll = "all"

	// WordSome is the word "some."
	WordSome = "some"

	// WordNo is the word "no."
	WordNo = "no"

	// WordNot is the word "not."
	WordNot = "not"
)

// IsNegative determines if this form is negative.
func (t Form) IsNegative() bool {
	// TODO: don't rely on numeric values here?
	// switch t {
	// case SomeAIsNotB:
	// 	fallthrough
	// case NoAIsB:
	// 	fallthrough
	// case AIsNotT:
	// 	return true
	// }
	return t%2 == 1
}

// Copula associated with this form.
// * => general term
// + => designator
// TODO: add some tests!
func (t Form) Copula() string {
	switch t {
	case SomeAIsB:
		return "  is"
	case SomeAIsNotB:
		return "  is not"
	case AllAIsB:
		return "  is"
	case NoAIsB:
		return "  is"
	case AIsT:
		return "  is"
	case AIsNotT:
		return "  is not"
	case AEqualsT:
		return "  = "
	case ADoesNotEqualT:
		return "   = / = "
	default:
		return ""
	}
}

// Quantifier associated with this form.
// TODO: add some tests!
func (t Form) Quantifier() string {
	switch t {
	case SomeAIsB:
		return WordSome
	case SomeAIsNotB:
		return WordSome
	case AllAIsB:
		return WordAll
	case NoAIsB:
		return WordNo
	case AIsT:
		return ""
	case AIsNotT:
		return ""
	case AEqualsT:
		return ""
	case ADoesNotEqualT:
		return ""
	default:
		return ""
	}
}

// Subject returns a symbol for term A associated with this form.
// * => general term
// + => designator
// TODO: add some tests!
func (t Form) Subject() string {
	switch t {
	case SomeAIsB:
		return ""
	case SomeAIsNotB:
		return ""
	case AllAIsB:
		return "*"
	case NoAIsB:
		return "*"
	case AIsT:
		return "+"
	case AIsNotT:
		return "+"
	case AEqualsT:
		return "+"
	case ADoesNotEqualT:
		return "+"
	default:
		return ""
	}
}

// Predicate symbol associated with this form.
// * => general term?
// + => designator?
// TODO: figure this out
// TODO: add some tests
func (t Form) Predicate() string {
	switch t {
	case SomeAIsB:
		return ""
	case SomeAIsNotB:
		return "*"
	case AllAIsB:
		return ""
	case NoAIsB:
		return "*"
	case AIsT:
		return ""
	case AIsNotT:
		return "*"
	case AEqualsT:
		return "+"
	case ADoesNotEqualT:
		return "*"
	default:
		return ""
	}
}

// func (t Type) String() string {
// 	switch t {
// 	case TypeGeneralTerm:
// 		return "general term"
// 	case TypeDesignator:
// 		return "designator"
// 	default:
// 		return "undetermined type"
// 	}
// }
