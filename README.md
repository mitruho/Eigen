<div align="center">
  
  ![logo](./data/icons/hicolor/scalable/apps/io.github.elahpeca.Eigen.svg)


  <h1>Eigen</h1>
  <b>Nice and simple matrix calculator</b>
</div>
<br>
<div align="center">
  
![Screenshot](./data/screenshots/screenshot1.png)

</div>
<br>
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
flatpak-builder --force-clean --user --install .flatpak/repo io.github.elahpeca.Eigen.json
```

```
flatpak run io.github.elahpeca.Eigen
```
