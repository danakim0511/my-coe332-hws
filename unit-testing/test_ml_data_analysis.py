from ml_data_analysis import compute_average_mass
import pytest

data_1 = [ {'thing' : 1}, {'thing' : 2} ]
data_2 = [ {'thing' : 30}, {'thing' : 40} ]
data_3 = [ {'mass' : 5}, {'mass' : 10} ] 

def test_compute_average_mass():
    assert( compute_average_mass(data_1, 'thing') == 1.5 )
    assert( compute_average_mass(data_2, 'thing') == 35 )
    assert( compute_average_mass(data_3, 'mass') == 7.5)
    
    assert( compute_average_mass ( [{'mass' :1}], 'mass') == 1)

    assert( isintance(compute_average_mass(data_3, 'mass'), float) == True )

def test_compute_average_mass_exceptions():
    with pytest.raises(ZeroDivisionError):
        compute_average_mass( [], 'a')
    with pytest.rasies(KeyError):
        compute_average_mass( [{'a': 1}, {'b':1}], 'a' )

def test_check_hemisphere():
    assert( check_hemisphere( 50.775, 6.08333) == 'Northern & Eastern' )
    assert( isinstance( check_hemisphere( 1, 1), str) == True)

