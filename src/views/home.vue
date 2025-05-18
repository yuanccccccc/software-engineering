<template>
  <div style="height: 100%">
    <div class="header" v-if="isLoggedIn">
      <div class="header-col left">
        <Menu
          mode="horizontal"
          @on-select="(name) => $route.name !== name && $router.push(name)"
          :active-name="$route.name"
        >
          <MenuItem name="main_info">主要信息</MenuItem>
          <MenuItem name="page2">水质数据</MenuItem>
          <MenuItem name="page4">鱼类数据</MenuItem>
        </Menu>
      </div>
      <div class="header-col center">
        <div class="header-title">智慧海洋牧场可视化系统</div>
      </div>
      <div class="header-col right">
        <Menu
          mode="horizontal"
          @on-select="(name) => $route.name !== name && $router.push(name)"
          :active-name="$route.name"
        >
          <MenuItem name="page3">数据中心</MenuItem>
          <MenuItem name="ig_center">智能中心</MenuItem>
          <MenuItem v-if="role === 'admin'" name="Admin">管理员页面</MenuItem>
        </Menu>
      </div>
    </div>
    <div class="page">
      <router-view v-if="flag" :selectRangeDate="selectRangeDate"></router-view>
    </div>
    <div class="footer" v-if="isLoggedIn">
      <Menu
        mode="horizontal"
        @on-select="handleSelect"
        :active-name="activeName"
      >
        <MenuItem name="day">昨日</MenuItem>
        <MenuItem name="week">近一周</MenuItem>
        <MenuItem name="month">近一月</MenuItem>
        <Submenu name="4">
          <template slot="title">
            <Icon type="ios-settings-outline" size="24" color="#60C2D4" />
          </template>
          <MenuItem name="filter">筛选</MenuItem>
        </Submenu>
      </Menu>
    </div>
    <Modal
      v-model="modal"
      title="选择时间"
      :mask-closable="false"
      @on-ok="getMonthBetween(startTime, endTime)"
    >
      <!-- ...existing code... -->
    </Modal>
  </div>
</template>

<script>
export default {
  name: "",
  data() {
    return {
      isLoggedIn: false,
      role: "",
      activeName: "month", // 默认显示近一月
      modal: false,
      flag: false,
      selectRangeDate: [],
      startTime: "",
      endTime: "",
      optionStart: {
        disabledDate(date) {
          // 禁止选择今天之后的日期
          return date && date.valueOf() > Date.now() - 86400000;
        },
      },
      optionEnd: {},
      resizeFn: null,
    };
  },
  mounted() {
    this.checkLoginStatus();
    window.addEventListener("resize", this.resizeFn);
    this.handleSelect(this.activeName); // 默认显示近一个月
  },
  methods: {
    checkLoginStatus() {
      const token = localStorage.getItem("token");
      const role = localStorage.getItem("role");
      if (token) {
        this.isLoggedIn = true; // 设置为已登录
        this.role = role; // 设置用户角色
      } else {
        this.isLoggedIn = false; // 确保未登录时为 false
      }
    },
    pickStartDate(date) {
      // 选择开始时间的回调
      this.startTime = date;
      this.optionEnd = {
        disabledDate(d) {
          // 禁止选择开始时间之前的日期
          return d && d.valueOf() < new Date(date).valueOf() - 86400000;
        },
      };
    },
    pickEndDate(date) {
      // 选择结束时间的回调
      this.endTime = date;
    },
    getMonthBetween(start, end) {
      // 获取开始时间和结束时间之内的所有月份
      this.selectRangeDate = [];
      let s = start.split("-"); // 字符串装换数组
      let e = end.split("-");
      let date = new Date();
      let min = date.setFullYear(s[0], s[1] - 1); // 设置最小时间
      let max = date.setFullYear(e[0], e[1] - 1); // 设置最大时间
      let curr = min;
      while (curr <= max) {
        // 循环添加月份
        var month = curr.getMonth();
        var arr = [curr.getFullYear(), month + 1];
        this.selectRangeDate.push(arr);
        curr.setMonth(month + 1);
      }
    },
    getDays(day) {
      // 获取天数
      let arr = [];
      for (let i = -day; i < 0; i++) {
        // 循环添加天数
        let today = new Date(); // 获取今天
        let targetday_milliseconds = today.getTime() + 1000 * 60 * 60 * 24 * i;
        today.setTime(targetday_milliseconds); //设置i天前的时间
        let tYear = today.getFullYear();
        let tMonth = today.getMonth();
        let tDate = today.getDate();
        let date = [tYear, tMonth + 1, tDate];
        arr.push(date);
      }
      return arr;
    },
    handleSelect(name) {
      switch (name) {
        case "day":
          break;
        case "week":
          this.selectRangeDate = this.getDays(7); // 获取近一周的天数
          this.flag = true;

          break;
        case "month":
          this.selectRangeDate = this.getDays(30); // 获取近一个月的天数
          this.flag = true;
          break;
        case "filter":
          this.modal = true;
          break;
        default:
          break;
      }
    },
  },
};
</script>

<style lang="less">
.ivu-modal {
  .ivu-modal-content {
    background: #071332;

    .ivu-modal-header {
      border-bottom: 1px solid #1a3c58;

      .ivu-modal-header-inner {
        color: #75deef;
      }
    }

    .ivu-modal-body {
      text-align: center;

      .ivu-icon {
        color: #75deef;
      }

      .ivu-modal-confirm-body {
        padding-left: 0;
        color: #75deef;
      }

      .ivu-input {
        background-color: rgba(0, 0, 0, 0);
        border: 1px solid #1a3c58;
        color: #75deef;

        &::-webkit-input-placeholder {
          /* WebKit, Blink, Edge */
          color: #75deef;
        }

        &::-moz-placeholder {
          /* Mozilla Firefox 4 to 18 */
          color: #75deef;
        }

        &::-moz-placeholder {
          /* Mozilla Firefox 19+ */
          color: #75deef;
        }

        &::-ms-input-placeholder {
          /* Internet Explorer 10-11 */
          color: #75deef;
        }
      }

      .ivu-picker-panel-body {
        background: #071332;

        .ivu-date-picker-header {
          color: #75deef;
          border-bottom: 1px solid #1a3c58;
        }

        .ivu-date-picker-cells-cell {
          color: #75deef;

          &:hover em {
            background: #1a3c58;
          }
        }

        .ivu-date-picker-cells-cell-disabled {
          background: rgba(0, 0, 0, 0);
          color: #eee;
        }

        .ivu-date-picker-cells-focused em {
          box-shadow: 0 0 0 1px #1a3c58 inset;

          &::after {
            background: #1a3c58;
          }
        }
      }
    }

    .ivu-modal-footer {
      border-top: 1px solid #1a3c58;

      .ivu-btn-primary {
        color: #75deef;
        background: #1a3c58;
      }

      .ivu-btn-text {
        color: #ddd;

        &:hover {
          color: #75deef;
          background: #1a3c58;
        }
      }
    }
  }
}

.header {
  height: 80px;
  background: #03044a;
  display: flex;
  align-items: center;
  .header-col {
    display: flex;
    align-items: center;
    height: 100%;
    &.left,
    &.right {
      flex: 1.5;
      justify-content: flex-start;
    }
    &.center {
      flex: 2;
      justify-content: center;
    }
    &.right {
      justify-content: flex-end;
    }
  }
  .header-title {
    color: #75deef;
    font-size: 30px;
    letter-spacing: 10px;
    text-align: center;
    white-space: nowrap;
  }
}

.footer {
  height: 60px;
  background: #03044a;
  display: flex;
  align-items: center;
  justify-content: center;
  .ivu-menu-horizontal {
    background: transparent;
  }
}

.page {
  height: calc(~"100% - 140px"); // 80px header + 60px footer
}
.header-col .ivu-menu-horizontal {
  line-height: 80px;
  height: 80px;
  background: transparent;
}

.ivu-menu-horizontal .ivu-menu-item,
.ivu-menu-horizontal .ivu-menu-submenu {
  color: #75deef;
  font-size: 18px;
  margin: 0 6px;
  background: transparent;
  transition: color 0.2s;
}

.ivu-menu-horizontal .ivu-menu-item-active {
  border-bottom: 2px solid #75deef;
  color: #fff;
}

.ivu-menu-horizontal .ivu-menu-item:hover,
.ivu-menu-horizontal .ivu-menu-submenu:hover {
  color: #fff;
  border-bottom: 2px solid #75deef;
}
</style>
