package article

// A Type holds an article type.
type Type int

// TODO: should be able to swap ordering of any of these and retain same functionality once refactor is complete
//       since we won't be relying on integer values anymore
const (
	// TypeNone represents no specific type.
	// TODO: is there a better way to name TypeNone?
	TypeNone Type = iota

	// TypeA represents a type preceded by the article "a."
	TypeA

	// TypeAn represents a type preceded by the article "an."
	TypeAn

	// TypeSm represents some quantity.
	TypeSm
)

func (t Type) String() string {
	switch t {
	case TypeA:
		return "a "
	case TypeAn:
		return "an "
	case TypeSm:
		return "sm "
	default:
		return ""
	}
}