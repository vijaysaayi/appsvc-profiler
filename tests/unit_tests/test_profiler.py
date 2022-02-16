import pytest
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