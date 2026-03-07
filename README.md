<div align="center">
  <img src="./data/icons/hicolor/scalable/apps/com.github.elahpeca.Eigen.svg" height="128"/><h1>Eigen</h1>
</div>
<b>Nice and simple matrix calculator</b>

Eigen is a GTK4 matrix calculator, designed with ease of use and elegance in mind.

It supports:

✅ Main matrix-matrix and matrix-scalar operations

✅ Transposition and matrix inversion

✅ Eigendecomposition, as well as other decompositions, such as QR, LU

<hr>

⚙️ Eigen uses NumPy matrix format, and makes working with them quite easy!

⚠️ Eigen is a very young app, so you're welcome to report the issues!
## Dependencies

- gtk4
- libadwaita1

## Building and running
#### Building requirements
- meson
- flatpak-builder

### Flatpak

Use Gnome Builder or run these commands in your terminal app to install flatpak.

```
flatpak-builder --force-clean --user --install .flatpak/repo com.github.elahpeca.Eigen.json
```

```
flatpak run com.github.elahpeca.Eigen
```
