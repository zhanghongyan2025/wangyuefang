import mysql.connector
from mysql.connector import Error


def delete_rooms_with_confirmation(base_config, databases, louyu_names, create_by):
    """
    查询并删除多个数据库中指定名称和创建者的楼宇记录，并在删除前进行预览和二次确认。

    :param base_config: 基础数据库连接配置（不含database名）。
    :param databases: 需要操作的数据库列表。
    :param louyu_names: 需要删除的楼宇名称列表。
    :param create_by: 创建者标识
    """
    # --- SQL语句 ---
    # 增加create_by条件过滤
    select_sql = """
    SELECT id, ms_id, lymc, create_time, create_by, 
           update_time, update_by, zt, zhcz, remark, 
           xzqh, xxdz, jd, wd

    FROM t_fwgl_louyu 
    WHERE lymc IN ({}) AND create_by = %s
    """.format(', '.join(['%s'] * len(louyu_names)))

    delete_sql = """
    DELETE FROM t_fwgl_louyu 
    WHERE lymc IN ({}) AND create_by = %s
    """.format(', '.join(['%s'] * len(louyu_names)))

    all_records = {}
    total_count = 0

    # --- 1. 数据预览阶段 ---
    print("\n" + "=" * 120)
    print("📋 待删除楼宇数据详情：")
    print("=" * 120)

    for db_name in databases:
        connection = None
        try:
            db_config = base_config.copy()
            db_config['database'] = db_name
            connection = mysql.connector.connect(**db_config)

            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)
                # 查询参数增加create_by
                query_params = louyu_names + [create_by]
                cursor.execute(select_sql, query_params)
                records = cursor.fetchall()

                if records:
                    all_records[db_name] = records
                    total_count += len(records)
                    print(f"\n🔍 数据库 [{db_name}] 中找到 {len(records)} 条匹配记录：")

                    # 定义列宽（可根据终端宽度调整）
                    col_widths = {"id": 30, "lymc": 60, "create_by": 30}
                    headers = ["ID", "楼宇名称", "创建者"]

                    # 打印表头
                    header_line = (
                        f"{headers[0]:<{col_widths['id']}} | "
                        f"{headers[1]:<{col_widths['lymc']}} | "
                        f"{headers[2]:<{col_widths['create_by']}} | "
                    )
                    print("-" * len(header_line))
                    print(header_line)
                    print("-" * len(header_line))

                    # 打印每条记录
                    for record in records:
                        # 截断过长文本
                        lymc = record.get('lymc', 'N/A')
                        if len(lymc) > col_widths['lymc']:
                            lymc = lymc[:col_widths['lymc'] - 3] + "..."

                        line = (
                            f"{str(record.get('id', 'N/A')):<{col_widths['id']}} | "
                            f"{lymc:<{col_widths['lymc']}} | "
                            f"{str(record.get('create_by', 'N/A')):<{col_widths['create_by']}} | "
                        )
                        print(line)
                    print("-" * len(header_line))
                else:
                    print(f"\nℹ️ 数据库 [{db_name}] 中未找到匹配记录")

        except Error as e:
            print(f"\n❌ 数据库 [{db_name}] 查询失败: {str(e)}")
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    if total_count == 0:
        print("\n" + "=" * 120)
        print("📌 没有找到任何匹配的楼宇记录，无需删除，程序退出。")
        print("=" * 120)
        return

    # --- 2. 二次确认阶段 ---
    print("\n" + "=" * 120)
    print(f"⚠️  确认要删除以上共 {total_count} 条楼宇记录吗？")
    print("   此操作不可逆，请谨慎确认！")
    print("=" * 120)

    while True:
        choice = input("请输入 (Y确认删除 / N取消)：").strip().upper()
        if choice in ['Y', 'N']:
            break
        print("❌ 输入无效，请输入 Y 或 N")

    # --- 3. 批量删除阶段 ---
    if choice == 'Y':
        print("\n" + "=" * 120)
        print("🚀 开始执行删除操作...")
        print("=" * 120)

        for db_name, records in all_records.items():
            connection = None
            try:
                db_config = base_config.copy()
                db_config['database'] = db_name
                connection = mysql.connector.connect(**db_config)

                if connection.is_connected():
                    cursor = connection.cursor()
                    # 删除参数增加create_by
                    delete_params = louyu_names + [create_by]
                    cursor.execute(delete_sql, delete_params)
                    connection.commit()
                    print(f"\n✅ 数据库 [{db_name}] 删除成功，共删除 {cursor.rowcount} 条记录")

            except Error as e:
                print(f"\n❌ 数据库 [{db_name}] 删除失败: {str(e)}")
                if connection:
                    connection.rollback()
            finally:
                if connection and connection.is_connected():
                    cursor.close()
                    connection.close()

        print("\n" + "=" * 120)
        print("📌 所有删除操作已完成")
        print("=" * 120)
    else:
        print("\n" + "=" * 120)
        print("📌 已取消删除操作，程序退出。")
        print("=" * 120)


if __name__ == "__main__":
    # --- 数据库配置 ---
    # ⚠️ 重要：在生产环境中，请不要硬编码密码！
    # 建议使用环境变量或配置文件来管理敏感信息。
    base_db_config = {
        'host': '192.168.40.60',
        'port': 3307,
        'user': 'root',
        'password': 'Cjzx_123456',
        'charset': 'utf8mb4'
    }

    # --- 操作目标 ---
    target_databases = ['us_wyfjgpt_fd', 'us_wyfjgpt_ga']
    # 将要删除的楼宇名称列表
    louyu_names_to_delete = ['1','123456789012345678901234567890', '123456789012345678901234567899']
    # 创建者标识
    create_by = '3700001152584814113861632'

    # --- 执行删除流程 ---
    delete_rooms_with_confirmation(base_db_config, target_databases, louyu_names_to_delete, create_by)