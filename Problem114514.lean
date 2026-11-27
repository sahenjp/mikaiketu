import Mathlib

/-!
Partial formalization of the 114514 problem.
No theorem asserting global existence or nonexistence is claimed.
Lean compilation is not yet verified; run lake env lean Problem114514.lean.
Finite computations use native_decide and its trusted evaluation mechanism.
-/

namespace Problem114514

set_option maxRecDepth 10000
set_option maxHeartbeats 0

structure Solution (p : ℕ) (a b c : ℤ) : Prop where
  prime : Nat.Prime p
  ge_five : 5 ≤ p
  a_nonzero : a ≠ 0
  b_nonzero : b ≠ 0
  c_nonzero : c ≠ 0
  gcd_ab : Int.gcd a b = 1
  gcd_bc : Int.gcd b c = 1
  gcd_ca : Int.gcd c a = 1
  equation : a ^ p + b ^ p + c ^ p = 114514

def ExistsSolution : Prop :=
  ∃ (p : ℕ) (a b c : ℤ), Solution p a b c

def Nonexistence : Prop := ¬ ExistsSolution

theorem reduce_equation (p q : ℕ) (a b c : ℤ)
    (h : a ^ p + b ^ p + c ^ p = 114514) :
    (a : ZMod q) ^ p + (b : ZMod q) ^ p + (c : ZMod q) ^ p =
      (114514 : ZMod q) := by
  simpa using congrArg (fun t : ℤ => (t : ZMod q)) h

theorem no_integer_solution_of_modular_obstruction (p q : ℕ)
    (h : ∀ x y z : ZMod q,
      x ^ p + y ^ p + z ^ p ≠ (114514 : ZMod q))
    (a b c : ℤ) : a ^ p + b ^ p + c ^ p ≠ 114514 := by
  intro heq
  exact h (a : ZMod q) (b : ZMod q) (c : ZMod q)
    (reduce_equation p q a b c heq)

private theorem mod11_p5 : ∀ x y z : ZMod 11,
    x ^ 5 + y ^ 5 + z ^ 5 ≠ (114514 : ZMod 11) := by
  native_decide

private theorem mod67_p11 : ∀ x y z : ZMod 67,
    x ^ 11 + y ^ 11 + z ^ 11 ≠ (114514 : ZMod 67) := by
  native_decide

private theorem mod53_p13 : ∀ x y z : ZMod 53,
    x ^ 13 + y ^ 13 + z ^ 13 ≠ (114514 : ZMod 53) := by
  native_decide

private theorem mod103_p17 : ∀ x y z : ZMod 103,
    x ^ 17 + y ^ 17 + z ^ 17 ≠ (114514 : ZMod 103) := by
  native_decide

private theorem mod47_p23 : ∀ x y z : ZMod 47,
    x ^ 23 + y ^ 23 + z ^ 23 ≠ (114514 : ZMod 47) := by
  native_decide

private theorem mod59_p29 : ∀ x y z : ZMod 59,
    x ^ 29 + y ^ 29 + z ^ 29 ≠ (114514 : ZMod 59) := by
  native_decide

theorem no_p5 (a b c : ℤ) : a ^ 5 + b ^ 5 + c ^ 5 ≠ 114514 :=
  no_integer_solution_of_modular_obstruction 5 11 mod11_p5 a b c

theorem no_p11 (a b c : ℤ) : a ^ 11 + b ^ 11 + c ^ 11 ≠ 114514 :=
  no_integer_solution_of_modular_obstruction 11 67 mod67_p11 a b c

theorem no_p13 (a b c : ℤ) : a ^ 13 + b ^ 13 + c ^ 13 ≠ 114514 :=
  no_integer_solution_of_modular_obstruction 13 53 mod53_p13 a b c

theorem no_p17 (a b c : ℤ) : a ^ 17 + b ^ 17 + c ^ 17 ≠ 114514 :=
  no_integer_solution_of_modular_obstruction 17 103 mod103_p17 a b c

theorem no_p23 (a b c : ℤ) : a ^ 23 + b ^ 23 + c ^ 23 ≠ 114514 :=
  no_integer_solution_of_modular_obstruction 23 47 mod47_p23 a b c

theorem no_p29 (a b c : ℤ) : a ^ 29 + b ^ 29 + c ^ 29 ≠ 114514 :=
  no_integer_solution_of_modular_obstruction 29 59 mod59_p29 a b c

theorem no_excluded_exponent (p : ℕ) (a b c : ℤ)
    (hp : p = 5 ∨ p = 11 ∨ p = 13 ∨ p = 17 ∨ p = 23 ∨ p = 29) :
    ¬ Solution p a b c := by
  intro h
  rcases hp with hp | hp | hp | hp | hp | hp
  · subst p
    exact no_p5 a b c h.equation
  · subst p
    exact no_p11 a b c h.equation
  · subst p
    exact no_p13 a b c h.equation
  · subst p
    exact no_p17 a b c h.equation
  · subst p
    exact no_p23 a b c h.equation
  · subst p
    exact no_p29 a b c h.equation

private theorem mod29_p7_constraint : ∀ x y z : ZMod 29,
    x ^ 7 + y ^ 7 + z ^ 7 = (114514 : ZMod 29) →
    x ^ 7 = 17 ∧ y ^ 7 = 17 ∧ z ^ 7 = 17 := by
  native_decide

theorem p7_residue_constraint (a b c : ℤ)
    (h : a ^ 7 + b ^ 7 + c ^ 7 = 114514) :
    (a : ZMod 29) ^ 7 = 17 ∧
    (b : ZMod 29) ^ 7 = 17 ∧
    (c : ZMod 29) ^ 7 = 17 :=
  mod29_p7_constraint (a : ZMod 29) (b : ZMod 29) (c : ZMod 29)
    (reduce_equation 7 29 a b c h)

theorem p7_mod29_witness :
    ∃ a b c : ℤ,
      a ≠ 0 ∧ b ≠ 0 ∧ c ≠ 0 ∧
      Int.gcd a b = 1 ∧ Int.gcd b c = 1 ∧ Int.gcd c a = 1 ∧
      (a : ZMod 29) ^ 7 + (b : ZMod 29) ^ 7 + (c : ZMod 29) ^ 7 = 114514 := by
  refine ⟨-2, -3, 55, ?_⟩
  native_decide

theorem gap_dvd (y d : ℤ) (p : ℕ) :
    d ∣ (y + d) ^ p - y ^ p := by
  induction p with
  | zero => simp
  | succ p ih =>
    obtain ⟨k, hk⟩ := ih
    refine ⟨(y + d) * k + y ^ p, ?_⟩
    calc
      (y + d) ^ (p + 1) - y ^ (p + 1) =
          (y + d) * ((y + d) ^ p - y ^ p) + d * y ^ p := by
            simp only [pow_succ]
            ring
      _ = d * ((y + d) * k + y ^ p) := by rw [hk]; ring

theorem gap_divides_target (x y d s : ℤ) (p : ℕ)
    (h : (y + d) ^ p - y ^ p = x ^ p + s * 114514) :
    d ∣ x ^ p + s * 114514 := by
  rw [← h]
  exact gap_dvd y d p

theorem gap_lower_bound (y d k : ℕ) :
    y ^ (k + 1) + (k + 1) * d * y ^ k ≤ (y + d) ^ (k + 1) := by
  induction k with
  | zero => simp
  | succ k ih =>
    calc
      y ^ (k + 1 + 1) + (k + 1 + 1) * d * y ^ (k + 1) ≤
          y ^ (k + 1 + 1) + (k + 1 + 1) * d * y ^ (k + 1) +
            (k + 1) * d * d * y ^ k := by omega
      _ = (y ^ (k + 1) + (k + 1) * d * y ^ k) * (y + d) := by
            simp only [pow_succ]
            ring
      _ ≤ (y + d) ^ (k + 1) * (y + d) := Nat.mul_le_mul_right _ ih
      _ = (y + d) ^ (k + 1 + 1) := (pow_succ (y + d) (k + 1)).symm

-- Open goals, intentionally not declared as theorems:
-- ExistsSolution or Nonexistence.
-- Next: prove sign normalization, p < min abs, p*d < x,
-- and link a verified finite-search certificate to an integer theorem.

#print axioms no_p5
#print axioms no_p29
#print axioms gap_dvd
#print axioms gap_lower_bound

end Problem114514
