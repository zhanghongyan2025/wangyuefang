import mysql.connector
from mysql.connector import Error


def delete_rooms_with_confirmation(base_config, databases, room_names):
    """
    查询并删除多个数据库中指定名称的房间记录，并在删除前进行预览和二次确认。

    :param base_config: 基础数据库连接配置（不含database名）。
    :param databases: 需要操作的数据库列表。
    :param room_names: 需要删除的房间名称列表。
    """
    # --- SQL语句 ---
    # 使用您提供的完整字段列表进行查询
    select_sql = """
    SELECT id, ms_id, ly_id, fjmc, cqlx, louceng, fxmc, fxmj, jyrlx, status, 
           chuangsl, zdzrs, has_cw, has_yt, has_ch, lock_code, create_time, 
           create_by, update_time, update_by, zt, bedrooms, livingrooms, 
           kitchens, bathrooms, xxdz, msmc, user_id, zhcz, remark, xzqh, 
           dd_id, dd_zt
    FROM t_fwgl_fjgl 
    WHERE fjmc IN ({})
    """.format(', '.join(['%s'] * len(room_names)))

    delete_sql = """
    DELETE FROM t_fwgl_fjgl 
    WHERE fjmc IN ({})
    """.format(', '.join(['%s'] * len(room_names)))

    all_records = {}
    total_count = 0

    # --- 1. 数据预览阶段 ---
    print("\n" + "=" * 120)
    print("📋 待删除房间数据详情：")
    print("=" * 120)

    for db_name in databases:
        connection = None
        try:
            db_config = base_config.copy()
            db_config['database'] = db_name
            connection = mysql.connector.connect(**db_config)

            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)
                cursor.execute(select_sql, room_names)
                records = cursor.fetchall()

                if records:
                    all_records[db_name] = records
                    total_count += len(records)
                    print(f"\n🔍 数据库 [{db_name}] 中找到 {len(records)} 条匹配记录：")
                    print("-" * 120)
                    # 调整输出表格，显示房间关键信息
                    print(f"{'ID':<6} {'房间名称':<20} {'所属楼宇':<10} {'楼层':<6} "
                          f"{'房间面积':<10} {'状态':<8} {'创建时间':<20}")
                    print("-" * 120)
                    for record in records:
                        # 安全地处理可能为None的字段
                        id_val = str(record.get('id', 'N/A'))
                        fjmc_val = record.get('fjmc', 'N/A')
                        ly_id_val = str(record.get('ly_id', 'N/A'))
                        louceng_val = record.get('louceng', 'N/A')
                        fxmj_val = str(record.get('fxmj', 'N/A'))
                        status_val = str(record.get('status', 'N/A'))
                        create_time_val = str(record.get('create_time', ''))[:19]

                        print(f"{id_val:<6} {fjmc_val:<20} {ly_id_val:<10} "
                              f"{louceng_val:<6} {fxmj_val:<10} {status_val:<8} "
                              f"{create_time_val:<20}")
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
        print("📌 没有找到任何匹配的房间记录，无需删除，程序退出。")
        print("=" * 120)
        return

    # --- 2. 二次确认阶段 ---
    print("\n" + "=" * 120)
    print(f"⚠️  确认要删除以上共 {total_count} 条房间记录吗？")
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
                    cursor.execute(delete_sql, room_names)
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
    room_names_to_delete = ['Test Room','民宿页面备案民宿_提交','民宿页面备案民宿_1','Test Room operation','view normal room','disable normal room', 'restore disabled room', 'log_off_room']

    # --- 执行删除流程 ---
    delete_rooms_with_confirmation(base_db_config, target_databases, room_names_to_delete)