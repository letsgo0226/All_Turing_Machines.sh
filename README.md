# All_Turing_Machines.sh

`All_Turing_Machines.sh` is a 2KB one-line universal dovetailer.

It reads two lines from stdin:

```text
N = finite machine/input prefix, blank defaults to 8
B = finite dovetailing stages, blank defaults to 16
```

The script enumerates the first `N` two-state/two-symbol Turing machines by integer index and the first `N` unary inputs `X_j = 1^j`. At each stage it fairly advances every pair `(M_i, X_j)` with `i + j <= stage`.

It outputs:

```text
All_Turing_Machines.clcert
```

The certificate records the finite population, bounded stages, recently executed trace entries, discovered finite `HALT` witnesses, and the closure fields `ZP`, `BUG`, `PCC`, and `ZE`.

This is not a halting oracle. It is a fair finite-prefix runner: any machine/input pair that halts inside the explored prefix and bound is reported with a witness.
