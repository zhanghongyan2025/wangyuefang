import mysql.connector
from mysql.connector import Error


def delete_users_with_confirmation(base_config, databases, usernames):
    """修复None值格式化问题，确保所有字段都能安全显示"""
    select_sql = """
    SELECT id, username, telephone, lxdh, realname, status, 
           create_time, last_login_time, sys_type, fd_type
    FROM t_sys_user 
    WHERE username IN ({})
    """.format(', '.join(['%s'] * len(usernames)))

    delete_sql = """
    DELETE FROM t_sys_user 
    WHERE username IN ({})
    """.format(', '.join(['%s'] * len(usernames)))

    all_records = {}
    total_count = 0

    print("\n" + "=" * 120)
    print("📋 待删除数据详情：")
    print("=" * 120)

    for db_name in databases:
        connection = None
        try:
            db_config = base_config.copy()
            db_config['database'] = db_name
            connection = mysql.connector.connect(**db_config)

            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)
                cursor.execute(select_sql, usernames)
                records = cursor.fetchall()

                if records:
                    all_records[db_name] = records
                    total_count += len(records)
                    print(f"\n🔍 数据库 [{db_name}] 中找到 {len(records)} 条匹配记录：")
                    print("-" * 120)
                    print(f"{'ID':<6} {'用户名':<30} {'手机号':<15} {'联系电话':<15} "
                          f"{'姓名':<10} {'状态':<6} {'系统类型':<8} {'创建时间':<20}")
                    print("-" * 120)
                    for record in records:
                        # 处理可能为None的字段，转换为字符串
                        id_val = str(record.get('id', 'N/A'))
                        username_val = record.get('username', 'N/A')
                        telephone_val = record.get('telephone', '')
                        lxdh_val = record.get('lxdh', '')
                        realname_val = record.get('realname', '')
                        # 关键修复：确保status不为None，转换为字符串
                        status_val = str(record.get('status', 'N/A'))
                        sys_type_val = record.get('sys_type', '')
                        # 处理时间字段为None的情况
                        create_time_val = str(record.get('create_time', ''))[:19]

                        # 格式化输出
                        print(f"{id_val:<6} {username_val:<30} "
                              f"{telephone_val:<15} {lxdh_val:<15} "
                              f"{realname_val:<10} {status_val:<6} "
                              f"{sys_type_val:<8} {create_time_val:<20}")
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
        print("📌 没有找到任何匹配的记录，无需删除，程序退出。")
        print("=" * 120)
        return

    print("\n" + "=" * 120)
    print(f"⚠️  确认要删除以上共 {total_count} 条记录吗？")
    print("   此操作不可逆，请谨慎确认！")
    print("=" * 120)

    while True:
        choice = input("请输入 (Y确认删除 / N取消)：").strip().upper()
        if choice in ['Y', 'N']:
            break
        print("❌ 输入无效，请输入 Y 或 N")

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
                    cursor.execute(delete_sql, usernames)
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
    base_db_config = {
        'host': '192.168.40.60',
        'port': 3307,
        'user': 'root',
        'password': 'Cjzx_123456',
        'charset': 'utf8mb4'
    }

    target_databases = ['us_wyfjgpt_fd', 'us_wyfjgpt_ga']
    usernames_to_delete = ['ab', 'abcdefghijklmnopqrstuvwxyzzzzz', "password_exactly_min_length_fd", "password_exactly_max_length_fd","password_valid_special_chars_f",
                           "password_valid_medium_fd", "password_valid_max_fd", "password_valid_min_fd", "test_verify_code","code_twice_sucess", "code_twice_expired", "code_expired_timeout","personal_person_tel_valid","personal_phone_number_valid",
                           "personal_phone_number_duplicat", "enterprise_phone_number_valid", "enterprise_legal_tel_valid", "personal_person_id_valid", "enterprise_legal_id_valid","enterprise_phone_number_duplic",
                           "personal_success_123","ent_success_456"]

    delete_users_with_confirmation(base_db_config, target_databases, usernames_to_delete)
