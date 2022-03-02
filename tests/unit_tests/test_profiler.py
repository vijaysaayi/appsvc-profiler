import pytest
from appsvc_profiler.constants import CodeProfilerConstants
from appsvc_profiler.profiler import CodeProfiler, ViztracerCodeProfiler

@pytest.mark.parametrize(
    "pid,time_to_profile",
    [
        pytest.param(10, 10)
    ]
    ) 
def test_viztracercodeprofiler_init(pid,time_to_profile):
    with pytest.raises(TypeError) as e:
        viztracer = ViztracerCodeProfiler()
        
    viztracer = ViztracerCodeProfiler(pid)
    assert type(viztracer.pid) == int
    assert viztracer.pid == pid
    
    assert type(viztracer.time_to_profile) == int
    assert viztracer.time_to_profile == 0
    
    viztracer = ViztracerCodeProfiler(pid, time_to_profile)
    assert type(viztracer.pid) == int
    assert viztracer.pid == pid
    
    assert type(viztracer.time_to_profile) == int
    assert viztracer.time_to_profile == time_to_profile

@pytest.mark.parametrize(
    "pid,time_to_profile",
    [
        pytest.param(10, 10)
    ]
    ) 
def test_viztracercodeprofiler_generate_command(pid,time_to_profile):
    viztracer = ViztracerCodeProfiler(pid)
    command = viztracer.generate_command()
    expected_command=["viztracer", "--attach", str(pid)]
    assert command == expected_command
        
    viztracer = ViztracerCodeProfiler(pid, time_to_profile)
    command = viztracer.generate_command()
    expected_command=["viztracer", "--attach", str(pid),"-t",str(time_to_profile)]
    assert command == expected_command

@pytest.mark.parametrize(
    "filepath,expected_result",
    [
        pytest.param("", False),
        pytest.param("filename", False),
        pytest.param("filename.txt", False),
        pytest.param("profiler_trace.json", False),
        pytest.param("/filename", True),
        pytest.param("/tmp/filename", True),
        pytest.param("/tmp/filename.txt", True)
    ]
    )  
def test_looks_like_absolute_path(filepath,expected_result):
    profiler = CodeProfiler(pid=0)
    assert profiler._looks_like_absolute_path(filepath) == expected_result
    
@pytest.mark.parametrize(
    "filepath,is_absolute_path",
    [
        pytest.param("profiler_trace.json", False),
        pytest.param("filename", False),
        pytest.param("filename.txt", False),
        pytest.param("/filename", True),
        pytest.param("/tmp/filename", True),
        pytest.param("/tmp/filename.txt", True)
    ]
    )  
def test_get_output_file_path(filepath,is_absolute_path):
    constants = CodeProfilerConstants()
    expected_result = filepath if is_absolute_path else f"{constants.CODE_PROFILER_LOGS_DIR}/{filepath}"
    
    profiler = CodeProfiler(pid=0, output_filename=filepath)
    assert profiler._get_output_file_path() == expected_result
    