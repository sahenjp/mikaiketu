import Mathlib

namespace TwoTargets

def Admissible (a b c : ℤ) : Prop :=
  a ≠ 0 ∧ b ≠ 0 ∧ c ≠ 0 ∧
  Int.gcd a b = 1 ∧ Int.gcd b c = 1 ∧ Int.gcd c a = 1

def HasSolutionAt (N : ℤ) (p : ℕ) : Prop :=
  Nat.Prime p ∧ 5 ≤ p ∧
  ∃ a b c : ℤ, Admissible a b c ∧ a ^ p + b ^ p + c ^ p = N

def HasSolution (N : ℤ) : Prop := ∃ p : ℕ, HasSolutionAt N p

theorem liftObstruction (N : ℤ) (p q : ℕ)
    (h : ∀ x y z : ZMod q, x ^ p + y ^ p + z ^ p ≠ (N : ZMod q))
    (a b c : ℤ) : a ^ p + b ^ p + c ^ p ≠ N := by
  intro heq
  apply h (a : ZMod q) (b : ZMod q) (c : ZMod q)
  simpa only [Int.cast_add, Int.cast_pow] using
    congrArg (fun t : ℤ => (t : ZMod q)) heq

private theorem mod11 : ∀ x y z : ZMod 11,
    x ^ 5 + y ^ 5 + z ^ 5 ≠ (114514 : ZMod 11) := by
  native_decide

private theorem mod29 : ∀ x y z : ZMod 29,
    x ^ 7 + y ^ 7 + z ^ 7 ≠ (364364 : ZMod 29) := by
  native_decide

theorem no114514p5 : ¬ HasSolutionAt 114514 5 := by
  rintro ⟨_, _, a, b, c, _, h⟩
  exact liftObstruction 114514 5 11 (by simpa using mod11) a b c h

theorem no364364p7 : ¬ HasSolutionAt 364364 7 := by
  rintro ⟨_, _, a, b, c, _, h⟩
  exact liftObstruction 364364 7 29 (by simpa using mod29) a b c h

-- Open targets: not asserted as theorems.
def Nonexistence114514 : Prop := ¬ HasSolution 114514
def Nonexistence364364 : Prop := ¬ HasSolution 364364

def LocallySolvable (N : ℤ) (p : ℕ) : Prop :=
  ∀ m : ℕ, 0 < m → ∃ a b c : ℤ, Admissible a b c ∧
    (a ^ p + b ^ p + c ^ p) % (m : ℤ) = N % (m : ℤ)

#print axioms no114514p5
#print axioms no364364p7

end TwoTargets
