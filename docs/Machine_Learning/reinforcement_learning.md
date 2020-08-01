
# Reinforcement learning 强化学习

- environment
- agent
- state： 系统的状态
- observation：agent可见的状态
- action
- reward
- policy: a function that maps states to actions
- episode
- trajectory: 一个episode中s,a,r构成的序列
- returns: discounted sum of future rewards

# environment

## CartPole
CartPole https://github.com/openai/gym/wiki/CartPole-v0
```python
import gym
env = gym.make('CartPole-v0')

# 获取初始状态
init_state = env.reset()
```



## CartPole in colab 
```
!apt-get install -y xvfb python-opengl
!pip install pyglet
!pip install pyvirtualdisplay
```

colab 动态刷新显示
```python
import pyvirtualdisplay
# Set up a virtual display for rendering OpenAI gym environments.
display = pyvirtualdisplay.Display(visible=0, size=(1400, 900)).start()

import gym
import numpy as np
import matplotlib.pyplot as plt
from IPython import display as ipythondisplay

env = gym.make("CartPole-v0")
env.reset()
prev_screen = env.render(mode='rgb_array')
plt.imshow(prev_screen)

def show_image(img):
  plt.imshow(img)
  ipythondisplay.clear_output(wait=True)
  ipythondisplay.display(plt.gcf())

for i in range(50):
  action = env.action_space.sample()
  obs, reward, done, info = env.step(action)
  screen = env.render(mode='rgb_array')

  show_image(screen)

  if done:
    break

ipythondisplay.clear_output(wait=True)
env.close()
```

tf-agents 环境
```python
import PIL.Image
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment

# 加载环境
env = suite_gym.load(env_name)

# 可视化环境
PIL.Image.fromarray(env.render())

# 环境规格信息，action_spec()可以获得可执行的动作
env.action_spec()
env.time_step_spec()
```
例如，如下的BoundedArraySpec，表示可执行动作的取值为0或1， 调用env.step(action)时，有效参数为0或1
```
BoundedArraySpec(shape=(), dtype=dtype('int64'), name=None, minimum=0, maximum=1)
```

## CartPole



# policy
policy: map an observation from the environment to an action or a distribution over actions

$\pi(a_t|s_t)$ 在t时刻，系统状态为$s_t$，选择执行动作$a_t$的函数



# rewards
maximize the sum of rewards $\sum^{T}_{t=0} \gamma^{t}r_{t}$, 

$\gamma$ - discount factor, [0,1]

# policy gradient, value-based, actor-critic
value-based - 评估在状态（state)下采取动作（action)获得的收益(reward)

policy gradient - 根据


# 强化学习分类（按照损失函数划分）
- `Temporal-Difference` : 例如`Q-learning`, 减少预测的Q值和真实Q值的误差， Q值是关于state和action的函数，表示在系统状态s下采取动作a能够获得的期望收益， value-based
- `Policy Gradients` ： 
- `actor-critic`: value-based 和 Policy Gradients 方法的混合， actor为policy， critic为Q值

## Q-Learning
Q-function (state-action value function)

optimal Q-function $Q^{*}(s, a)$: maximum return that can be obtained starting from observation $s$

Bellman optimality equation

$Q^{*}(s, a) = E [ r + \gamma max_{a'}Q^*(s', a')]$

```
s - current state
a - current action
r - immediate reward
s' - next state after a
a' - next action after a
E - expectation 
```

当前收益，和下一步所处状态可能收益的期望


## Deep Q-Learning

optimal Q-function $Q^{*}(s, a; \theta)$ 用神经网络模拟Q值函数

$L(\theta) = E_{s,a,r,s' ~p(.)}[(y_i - Q(s,a;\theta_i))^2]$ 

$y_i = r + \gamma max_{a'}Q(s', a';\theta_{i-1})$

$y_i$ - TD (temporal difference) target

p(.) -  behaviour distribution

## 策略梯度policy gradient

轮次奖励 - 一个轮次中依次动作产生的奖励的总和

在一轮的学习中使用同一个策略直到该轮结束

每个策略会求多个轮次奖励的平均值


# actor-critic

## Advantage Actor-Critic (A2C)
## Asynchronous Advantage Actor-Critic (A3C)

gradients are weighted with `returns`: a discounted sum of future rewards

advantage function 优势函数

advantages = returns - values()

entropy maximization

class Model
输入为observation， 输出为action


```python
    def _returns_advantages(self, rewards, dones, values, next_value):
        # next_value is the bootstrap value estimate of a future state (the critic)
        returns = np.append(np.zeros_like(rewards), next_value, axis=-1)
        # returns are calculated as discounted sum of future rewards
        for t in reversed(range(rewards.shape[0])):
            returns[t] = rewards[t] + self.params['gamma'] * returns[t+1] * (1-dones[t])
        returns = returns[:-1]
        # advantages are returns - baseline, value estimates in our case
        advantages = returns - values
        return returns, advantages
```

episode 样本收集
episode需要包括，observation, action，reward的信息


```python
   def train(self, env, batch_sz=32, updates=1000):
        # storage helpers for a single batch of data
        actions = np.empty((batch_sz,), dtype=np.int32)
        rewards, dones, values = np.empty((3, batch_sz))
        observations = np.empty((batch_sz,) + env.observation_space.shape)
        # training loop: collect samples, send to optimizer, repeat updates times
        ep_rews = [0.0]
        next_obs = env.reset()
        for update in range(updates):
            for step in range(batch_sz):
                observations[step] = next_obs.copy()
                actions[step], values[step] = self.model.action_value(next_obs[None, :])
                next_obs, rewards[step], dones[step], _ = env.step(actions[step])

                ep_rews[-1] += rewards[step]
                if dones[step]:
                    ep_rews.append(0.0)
                    next_obs = env.reset()

            _, next_value = self.model.action_value(next_obs[None, :])
            returns, advs = self._returns_advantages(rewards, dones, values, next_value)
            # a trick to input actions and advantages through same API
            acts_and_advs = np.concatenate([actions[:, None], advs[:, None]], axis=-1)
            # performs a full training step on the collected batch
            # note: no need to mess around with gradients, Keras API handles it
            losses = self.model.train_on_batch(observations, [acts_and_advs, returns])
        return ep_rews
```



## Resource
http://spinningup.openai.com/en/latest/

tensorflow2.0 actor-critic
http://inoryy.com/post/tensorflow2-deep-reinforcement-learning/