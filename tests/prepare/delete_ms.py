import mysql.connector
from mysql.connector import Error


def delete_rooms_with_confirmation(base_config, databases, minsu_names):
    """
    查询并删除多个数据库中指定名称的房间记录，并在删除前进行预览和二次确认。

    :param base_config: 基础数据库连接配置（不含database名）。
    :param databases: 需要操作的数据库列表。
    :param minsu_names: 需要删除的民宿名称列表。
    """
    # --- SQL语句 ---
    # 使用您提供的完整字段列表进行查询
    select_sql = """
    SELECT id, user_id, msmc, xzqh, xxdz, ba_bh, ba_zt, 
           ba_time, shr_id, shrmc, shjg, shsj, shyj, create_time, 
           create_by, update_time, update_by, zt, zhcz, remark, tjsj
    FROM t_fwgl_minsu 
    WHERE msmc IN ({})
    """.format(', '.join(['%s'] * len(minsu_names)))

    delete_sql = """
    DELETE FROM t_fwgl_minsu 
    WHERE msmc IN ({})
    """.format(', '.join(['%s'] * len(minsu_names)))

    all_records = {}
    total_count = 0

    # --- 1. 数据预览阶段 ---
    print("\n" + "=" * 120)
    print("📋 待删除民宿数据详情：")
    print("=" * 120)

    for db_name in databases:
        connection = None
        try:
            db_config = base_config.copy()
            db_config['database'] = db_name
            connection = mysql.connector.connect(**db_config)

            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)
                cursor.execute(select_sql, minsu_names)
                records = cursor.fetchall()

                if records:
                    all_records[db_name] = records
                    total_count += len(records)
                    print(f"\n🔍 数据库 [{db_name}] 中找到 {len(records)} 条匹配记录：")

                    # 定义列宽（可根据终端宽度调整）
                    col_widths = {"id": 30, "msmc": 60, }
                    headers = ["ID", "民宿名称"]

                    # 打印表头
                    header_line = (
                        f"{headers[0]:<{col_widths['id']}} | "
                        f"{headers[1]:<{col_widths['msmc']}} | "
                    )
                    print("-" * len(header_line))
                    print(header_line)
                    print("-" * len(header_line))

                    # 打印每条记录
                    for record in records:
                        # 截断过长文本
                        msmc = record.get('msmc', 'N/A')
                        if len(msmc) > col_widths['msmc']:
                            msmc = msmc[:col_widths['msmc'] - 3] + "..."

                        line = (
                            f"{str(record.get('id', 'N/A')):<{col_widths['id']}} | "
                            f"{msmc:<{col_widths['msmc']}}  "
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
        print("📌 没有找到任何匹配的民宿记录，无需删除，程序退出。")
        print("=" * 120)
        return

    # --- 2. 二次确认阶段 ---
    print("\n" + "=" * 120)
    print(f"⚠️  确认要删除以上共 {total_count} 条民宿记录吗？")
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
                    cursor.execute(delete_sql, minsu_names)
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
    # 将要删除的房间名称列表
    room_names_to_delete = ['详细地址1个字符的民宿','详细地址刚好50个字符的民宿','短','这是一个刚好三十个字符的民宿名称用于测试长度限制', 'minsu_without_room', 'minsu_with_room', 'minsu_filing_submit', 'minsu_filing_submit', '民宿_提交_备案']

    # --- 执行删除流程 ---
    delete_rooms_with_confirmation(base_db_config, target_databases, room_names_to_delete)