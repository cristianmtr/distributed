#include <iostream>
#include <stdlib.h> //atoi
#include <vector>
#include <string>
#include <fstream>
#include <boost/python.hpp>

template<class T>
boost::python::list std_vector_to_py_list(const std::vector<T>& v)
{
    boost::python::object get_iter = boost::python::iterator<std::vector<T> >();
    boost::python::object iter = get_iter(v);
    boost::python::list l(iter);
    return l;
}

using namespace std;

int my_convert_string_to_int(string str)
{
  using namespace std;
  // cout << "converting " << str << endl;
  return atoi(str.c_str());
}

boost::python::list my_extract(string data)
{
  using namespace std;
  int len_map;
  int len_mapinput;
  int len_distributor;
  int len_reducer;

  string map_task;
  string map_input;
  string distributor_task;
  string reducer_task;

  // we know that we only need the first 4 ints
  // that are separated by comma
  // let's just do this by hand
  
  int i = 0;
  // this will keep count of how many commas we have encountered 
  // we stop at 3, 4 cases in total
  
  int j = 0;
  //this will be the index to parse the data string

  int last_point = 0;
  // this will hold the last point (index of data)
  // at which relevant data was found
  // important in order to calculate positions
  
  while (i != 4)
    {

      
      if (data[j] == ',')
	{
	  ++ i;

	  
	  switch (i)
	    {
	    case 1:
	      len_map = my_convert_string_to_int(data.substr(last_point, j));
	      // cout << len_map << endl;
	      break;
	      
	    case 2:
	      len_mapinput = my_convert_string_to_int(data.substr(last_point, j-last_point));
	      // cout << len_mapinput << endl;
	      break;
	      
	    case 3:
	      len_distributor = my_convert_string_to_int(data.substr(last_point, j-last_point));
	      // cout << len_distributor << endl;
	      break;
	      
	    case 4:
	      len_reducer = my_convert_string_to_int(data.substr(last_point, j-last_point));
	      // cout << len_reducer << endl;
	      break;
	      
	    }
	  // because substr() will start with the char in
	  // that position
	  last_point = j + 1;
	  // cout << "[j] was " << data[j] << endl;
	}
      
      ++ j;

    }
  map_task = data.substr(last_point, len_map);
  last_point = last_point + len_map;
  map_input = data.substr(last_point, len_mapinput);
  last_point = last_point + len_mapinput;
  distributor_task = data.substr(last_point, len_distributor);
  last_point = last_point + len_distributor;
  reducer_task = data.substr(last_point, len_reducer);

  boost::python::list python_list_of_results;

  python_list_of_results.append(map_task);
  python_list_of_results.append(map_input);
  python_list_of_results.append(distributor_task);
  python_list_of_results.append(reducer_task);
  
  return python_list_of_results;

}

// int main()
// {
//   string data;
//   string line;
//   ifstream myfile ("data.txt");
//   if (myfile.is_open())
//     {
//     while (getline (myfile, line))
//       {
//       data += line  + "\n";
//       }
//     myfile.close();
//     // cout << data;
//     }
//   else
//     { cout << "error opening" << endl; }
  
//   vector<string> temp = extract(data);
//   return 0;
// }

#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
using namespace boost::python;

BOOST_PYTHON_MODULE(module)
{
  // to_python_converter<std::vector<std::string,class std::allocator<std::string> >, VecToList<std::string> >();
  def("my_extract", my_extract);
  // def("do_multiply", do_multiply);
}

