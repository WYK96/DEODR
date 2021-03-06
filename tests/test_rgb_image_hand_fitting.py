"""Test using rgb_image hand fitting."""

from deodr.examples.rgb_image_hand_fitting import run


def test_rgb_image_hand_fitting_pytorch():

    energies = run(
        dl_library="pytorch",
        plot_curves=False,
        display=False,
        save_images=False,
        max_iter=50,
    )
    assert abs(energies[49] - 2106.5436357944604) < 12


def test_rgb_image_hand_fitting_numpy():

    energies = run(
        dl_library="none",
        plot_curves=False,
        display=False,
        save_images=False,
        max_iter=50,
    )
    assert abs(energies[49] - 2113.7013184079137) < 2


def test_rgb_image_hand_fitting_tensorflow():

    energies = run(
        dl_library="tensorflow",
        plot_curves=False,
        display=False,
        save_images=False,
        max_iter=50,
    )
    assert abs(energies[49] - 2107.0089187104204) < 1


if __name__ == "__main__":

    test_rgb_image_hand_fitting_pytorch()
    test_rgb_image_hand_fitting_numpy()
    test_rgb_image_hand_fitting_tensorflow()
