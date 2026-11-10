%global         repo_name RapidOCR
%global         alt_pypi_name python3-%{srcname}
%global         pypi_name %name
%global         srcname %(v="%{repo_name}"; echo "${v,,}")

Name:           python-%{srcname}
Version:        3.10.0
Release:        1%{?dist}
Summary:        Awesome OCR Library

License:        Apache-2.0
URL:            https://github.com/RapidAI/%{repo_name}

Source:         %{url}/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  pkgconfig pkgconfig(python)
BuildRequires:  python3dist(setuptools-scm)
BuildRequires:  python3dist(wheel)
BuildRequires:  python3dist(shapely)
BuildRequires:  python3dist(omegaconf)
BuildRequires:  python3dist(colorlog)
BuildRequires:  python3dist(opencv)
BuildRequires:  python3dist(pillow)
BuildRequires:  python3dist(pyclipper)
BuildRequires:  python3dist(tqdm)
BuildRequires:  python3dist(pip)

# Test dependencies
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(onnxruntime)

%description
Open source OCR for the security of the digital world.

%package -n     %{alt_pypi_name}
Summary:        %{summary}

%description -n %{alt_pypi_name}
Open source OCR for the security of the digital world.


%prep
%autosetup -p1 -n ./%{repo_name}-%{version}/python

# Fix dep on opencv
sed -i ./requirements.txt -e 's/opencv-python-headless/opencv/'


%generate_buildrequires
export SETUPTOOLS_SCM_PRETEND_VERSION=%version
%pyproject_buildrequires


%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%version
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files '%srcname'


%check
# Only the onnxruntime inference engine is needed by immich-machine-learning
%pyproject_check_import -e 'rapidocr.inference_engine.mnn*' -e 'rapidocr.inference_engine.openvino*' -e 'rapidocr.inference_engine.paddle*' -e 'rapidocr.inference_engine.pytorch*' -e 'rapidocr.inference_engine.tensorrt*'
# Tests that run OCR need to download models from the internet, also skip
# tests for inference engines that are not available in Fedora
%pytest -v --import-mode=append -p no:cacheprovider \
  --ignore=tests/test_cls.py \
  --ignore=tests/test_det_cls_rec.py \
  --ignore=tests/test_engine.py \
  --ignore=tests/test_rec_language.py \
  --ignore=tests/test_return_word.py \
  --ignore=tests/test_to_other_format.py \
  --ignore=tests/test_vis.py \
  --ignore=tests/test_engine_config.py \
  --deselect='tests/test_cli.py::test_cli[' \
  --deselect=tests/test_cli.py::test_cli_download_models \
  --deselect=tests/test_cli.py::test_cli_vis[ \
  --deselect=tests/test_cli.py::test_cli_lang_type \
  --deselect=tests/test_default_config.py::test_default_engine_real_full_pipeline \
  --deselect=tests/test_default_config.py::test_default_engine_real_rec_only \
  --deselect=tests/test_input.py::test_exif_transpose \
  --deselect=tests/test_input.py::test_full_black_img \
  --deselect=tests/test_input.py::test_img_url_input \
  --deselect=tests/test_input.py::test_input_bytes \
  --deselect=tests/test_input.py::test_input_memory_image \
  --deselect=tests/test_input.py::test_input_memory_image_matches_bytes \
  --deselect=tests/test_input.py::test_input_parameters \
  --deselect=tests/test_input.py::test_input_path \
  --deselect=tests/test_input.py::test_input_raw_memory_image \
  --deselect=tests/test_input.py::test_input_str \
  --deselect=tests/test_input.py::test_input_three_ndim_one_channel \
  --deselect=tests/test_input.py::test_input_three_ndim_two_channel \
  --deselect=tests/test_input.py::test_letterbox_like \
  --deselect=tests/test_input.py::test_long_img \
  --deselect=tests/test_input.py::test_mode_one_img \
  --deselect=tests/test_input.py::test_transparent_img \
  --deselect=tests/test_input.py::test_zeros


%files -n %{alt_pypi_name} -f %{pyproject_files}
%{_bindir}/%{srcname}
%doc ./README.md
%license ./LICENSE

%changelog
%autochangelog

