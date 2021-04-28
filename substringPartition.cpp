#include <iostream>
#include <functional>
#include <string>
#include <array>
#include <vector>

typedef std::vector<std::string> substring_partition_t;

void forEachSubstringPartition(std::string universe_string, std::function<void(substring_partition_t)> fn) {
    constexpr int num_masks = 32;
    std::array<uint32_t, num_masks> masks;
    for (int i = 0; i < num_masks; ++i) {
        masks[i] = 1 << i;
    }
    const int len_universe_string = universe_string.length();
    const int num_divisible = len_universe_string - 1;
    const uint32_t num_loop = 1 << num_divisible;
    for (uint32_t division_bits = 0; division_bits < num_loop; ++division_bits) {
        substring_partition_t parts;
        int tmp_part_index = 0;
        int tmp_part_len   = 1;
        for (int j = 0; j < num_divisible; ++j) {
            if (division_bits & masks[j]) {
                parts.push_back(universe_string.substr(tmp_part_index, tmp_part_len));
                tmp_part_index += tmp_part_len;
                tmp_part_len = 1;
            } else {
                ++tmp_part_len;
            }
        }
        parts.push_back(universe_string.substr(tmp_part_index));
        fn(parts);
    }
}

void printParts(substring_partition_t parts) {
    std::cout << "{";
    for (const auto& part: parts) {
        std::cout << "\"" << part << "\", ";
    }
    std::cout << "}" << std::endl;
}

int main() {
    std::string input;
    std::cin >> input;
    constexpr int len_input_limit = 10;
    if (input.length() > len_input_limit) {
        return 0;
    }
    forEachSubstringPartition(input, printParts);
    return 0;
}