from index import app, generate_random_number,update_countdown

# 在启动服务器之前执行所需操作
generate_random_number()
update_countdown()

# 启动服务器
if __name__ == '__main__':
    app.run(port=8899, debug=True)