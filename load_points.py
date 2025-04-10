def read_point_cloud_from_txt(file_path, delimiter=','):
    """
    从给定路径读取TXT格式的点云数据
    :param file_path: 点云数据文件的路径
    :param delimiter: 坐标之间的分隔符，默认为逗号
    :return: 点云数据列表，每个点为一个三元组(x, y, z)
    """
    point_cloud = []
    
    with open(file_path, 'r') as file:
        for line in file:
            # 使用指定的分隔符分割每行
            parts = line.strip().split(delimiter)
            if len(parts) == 3:
                try:
                    x = float(parts[0])
                    y = float(parts[1])
                    z = float(parts[2])
                    point_cloud.append((x, y, z))
                except ValueError:
                    print(f"无法转换为浮点数: {line.strip()}")
    
    return point_cloud
